
import os
import pandas as pd
import sys
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pickle

players = {}

# Function to get command-line parameters
def getParameters():
    if len(sys.argv) == 2:
        return sys.argv[1]
    else:
        print("Exactly two values must be provided as arguments.")
        sys.exit(1)
    
#Get valid id nodes   
def getValidId(dataFrame):
    # Remove NaN values from the 'player_id' column
    validRecipientId = dataFrame.loc[dataFrame['pass_recipient_id'].notna()]
    validPlayerIds = validRecipientId["player_id"].dropna().unique()

    # Convert each element to a float first, then to an integer
    keysAsFloat = np.array(validPlayerIds, dtype=float)
    keysAsInt = np.round(keysAsFloat).astype(int)

    return keysAsInt

# Define your function to get node attributes
def getNodeAttributes(dataFrame):
    # Extract unique players from the DataFrame
    uniquePlayers = dataFrame[['player_id', 'player_name']].drop_duplicates().dropna()
    # Initialize an empty dictionary for attributes
    attributes = {}
    # Iterate over the rows of the DataFrame
    for index, row in uniquePlayers.iterrows():
        # Convert player_id to integer
        player_id = int(float(row['player_id']))  # Convert to float first, then to int
        player_name = row['player_name']
        # Add the attribute for the current player to the dictionary
        attributes[player_id] = {"label": player_name}
    return attributes

def savePalyers(dict1):
    global players
    new_keys = set(dict1.keys()) - set(players.keys())
    # Update dict1 with the labels from dict2 for the new keys
    for key in new_keys:
        players[key] = dict1[key]['label']


def directedEdges(dataframe, G):
    uniquePlayers = dataframe[['player_id', 'pass_recipient_id']].drop_duplicates().dropna()
    # Convert player IDs and recipient IDs from strings that might represent floats to integers
    uniquePlayers['player_id'] = uniquePlayers['player_id'].astype(float).astype(int)
    uniquePlayers['pass_recipient_id'] = uniquePlayers['pass_recipient_id'].astype(float).astype(int)

    # Group by 'player_id' and 'pass_recipient_id', and count occurrences
    edge_weights = uniquePlayers.groupby(['player_id', 'pass_recipient_id']).size().reset_index(name='weight')
    
    # Ensure the weight is integer
    edge_weights['weight'] = edge_weights['weight'].astype(int)
    
    # Add edges to the graph with their weights
    # Convert DataFrame to list of tuples (node1, node2, weight)
    edge_list = edge_weights.to_records(index=False)
    G.add_weighted_edges_from(edge_list)


def add_edges_with_attributes(row, G):
    # Extract relevant information
    playerId = int(float(row['player_id']))
    passRecipientId = int(float(row['pass_recipient_id']))    
    attributes = {
        'possession': float(row['possession']),
        'location_0': float(row['location_0']),
        'location_1': float(row['location_1']),
        'pass_length': float(row['pass_length']),
        'pass_height_id': float(row['pass_height_id']),
        'pass_end_location_0': float(row['pass_end_location_0']),
        'pass_end_location_1': float(row['pass_end_location_1']),
        'pass_outcome_name': str(row['pass_outcome_name'])
    }  
    # Add edge with attributes to the graph
    G.add_edge(playerId, passRecipientId, **attributes)


# Function to change file names to a new format
def changeFilenames(fileName, type):
    # Check if the file name follows the pattern "Football_day_{jornada_value}_{i+1}.json"   
    if fileName.endswith(".csv"):
        parts = fileName.split("_")
        if len(parts) == 4  and parts[3] == "footballDayPasses.csv":
            newFileName = f"{parts[0]}_{parts[1]}_{parts[2]}_{type}.gexf"
            return newFileName
        elif len(parts) == 5  and parts[4] == "footballDayPasses.csv":
            newFileName = f"{parts[0]}_{parts[1]}_{parts[2]}_{parts[3]}_{type}.gexf"
            return newFileName
        else:
            print("The file name does not follow the expected pattern.")
            return None
    else:
        print("The file name does not have a CSV extension.")
        return None

def saveGraph(targetPath, G, fileName):
    # Combine the directory path and file name
    outputFilePath = os.path.join(targetPath, fileName)

    # Write the graph to the GraphML file
    nx.write_gexf(G, outputFilePath, version="1.2draft", encoding="utf-8", prettyprint=True)


def managmentMultiGraph(dataFrame, fileName, targetFolder, G):
    #Get valid ID nodes
    validPlayersIDs = getValidId(dataFrame)
    #Add nodes to the graph
    G.add_nodes_from(validPlayersIDs)
    #Get nodes attributes
    attributes = getNodeAttributes(dataFrame)
    #Add node's attributs
    nx.set_node_attributes(G, attributes)
    #Add edges and their attributs
    validRecipientId = dataFrame.loc[dataFrame['pass_recipient_id'].notna()]
    _ = validRecipientId.apply(add_edges_with_attributes, args=(G,), axis=1)
    #Verification
    assert len(list(G.edges())) == len(validRecipientId), f"number of edges and dataframe' size is not the same"
    #Get new fileName
    newFileName = changeFilenames(fileName, "multiDiGraph")
    #Save graph
    saveGraph(targetFolder, G, newFileName)
    

 

def managmentDiGraph(dataFrame, fileName, targetFolder, G):
    #Get valid ID nodes
    validPlayersIDs = getValidId(dataFrame)
    #Add nodes to the graph
    G.add_nodes_from(validPlayersIDs)
    #Get nodes attributes
    attributes = getNodeAttributes(dataFrame)
    savePalyers(attributes)
    #Add node's attributs
    nx.set_node_attributes(G, attributes)
    #Add edges 
    directedEdges(dataFrame, G)
    #Get new fileName
    newFileName = changeFilenames(fileName, "diGraph")
    #Save graph
    saveGraph(targetFolder, G, newFileName)
   

# Function to generate dynamic paths for data and target folders
def generateDynamicPaths(experimentName):
    currentDir = os.path.abspath(
        os.path.dirname(__file__)
    )  # Get the current directory of the script

    dataFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "03Stage", "TargetFiles"
    )
    targetFolderPlayers = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "04Stage"
    )
    targetFolderDi = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "04Stage", "Graphs", "diGraphs"
    )
    
    targetFolderMultiDi = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "04Stage", "Graphs", "multiDiGraphs"
    )

    if not os.path.exists(targetFolderDi):
        print(
            f"The folder {targetFolderDi} does not exist for experiment {experimentName}."
        )
        sys.exit(1)
    
    if not os.path.exists(targetFolderMultiDi):
        print(
            f"The folder {targetFolderMultiDi} does not exist for experiment {experimentName}."
        )
        sys.exit(1)

    return dataFolder, targetFolderPlayers, targetFolderDi, targetFolderMultiDi

def savePlayersAsObject(targetFolder):
    try:
        with open(f'{targetFolder}/playersList.pkl', 'wb') as f:
            pickle.dump(players, f)
        print("Metrics saved successfully.")
    except Exception as e:
        print("Error occurred while saving metrics:", str(e))

# Function to read files in a folder and process them
def readFolderFiles(currentPath, targetFolderDi, targetFolderMultiDi):
    # Check if the folder exists
    if not os.path.isdir(currentPath):
        print(f"The folder '{currentPath}' does not exist.")
        return

    # Iterate through all the files in the folder
    for fileName in os.listdir(currentPath):
        # Join the folder path with the file name
        filePath = os.path.join(currentPath, fileName)
        df = pd.read_csv(filePath, dtype=str)
        # Initialize a directed graph using NetworkX
        multiDiG = nx.MultiDiGraph()
        # Initialize a directed graph using NetworkX
        diG = nx.DiGraph()
        managmentDiGraph(df,fileName, targetFolderDi, diG)
        managmentMultiGraph(df,fileName,targetFolderMultiDi, multiDiG)


# Main function to execute the program
def main():
    experimentName = getParameters()
    dataFolder, targetFolderPlayers, targetFolderDi, targetFolderMultiDi = generateDynamicPaths(experimentName)
    readFolderFiles(dataFolder, targetFolderDi, targetFolderMultiDi)
    savePlayersAsObject(targetFolderPlayers)



if __name__ == "__main__":
    main()
