
import os
import pandas as pd
import sys
import networkx as nx
import numpy as np


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

#Get node attributs
def getNodeAttriutes(dataFrame):
    uniquePlayers = dataFrame[['player_id', 'player_name']].drop_duplicates().dropna()
    # Create a dictionary mapping player IDs to their names
    playerNameDict = dict(zip(uniquePlayers['player_id'], uniquePlayers['player_name']))
    return playerNameDict

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
def changeFilenames(fileName):
    # Check if the file name follows the pattern "Football_day_{jornada_value}_{i+1}.json"   
    if fileName.endswith(".csv"):
        parts = fileName.split("_")
        if len(parts) == 4  and parts[3] == "footballDayPasses.csv":
            newFileName = f"{parts[0]}_{parts[1]}_{parts[2]}_Graph.graphml"
            return newFileName
        elif len(parts) == 5  and parts[4] == "footballDayPasses.csv":
            newFileName = f"{parts[0]}_{parts[1]}_{parts[2]}_{parts[3]}_Graph.graphml"
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
    

def managmentGraph(dataFrame, fileName, targetFolder):
    # Initialize a directed graph using NetworkX
    G = nx.MultiDiGraph()
    #Get valid ID nodes
    validPlayersIDs = getValidId(dataFrame)
    #Add nodes to the graph
    G.add_nodes_from(validPlayersIDs)
    #Get nodes attributes
    attributes = getNodeAttriutes(dataFrame)
    #Add node's attributs
    nx.set_node_attributes(G, attributes, name='label')
    #Add edges and their attributs
    validRecipientId = dataFrame.loc[dataFrame['pass_recipient_id'].notna()]
    _ = validRecipientId.apply(add_edges_with_attributes, args=(G,), axis=1)
    #Verification
    assert len(list(G.edges())) == len(validRecipientId), f"number of edges and dataframe' size is not the same"
    #Get new fileName
    newFileName = changeFilenames(fileName)
    #Save graph
    saveGraph(targetFolder, G, newFileName)
    
    

# Function to generate dynamic paths for data and target folders
def generateDynamicPaths(experimentName):
    currentDir = os.path.abspath(
        os.path.dirname(__file__)
    )  # Get the current directory of the script

    dataFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "ThirdStage", "TargetFiles"
    )

    targetFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "XStage", "Graphs"
    )

    if not os.path.exists(targetFolder):
        print(
            f"The folder {targetFolder} does not exist for experiment {experimentName}."
        )
        sys.exit(1)

    return dataFolder, targetFolder


# Function to read files in a folder and process them
def readFolderFiles(currentPath, targetFolder):
    # Check if the folder exists
    if not os.path.isdir(currentPath):
        print(f"The folder '{currentPath}' does not exist.")
        return

    # Iterate through all the files in the folder
    for fileName in os.listdir(currentPath):
        # Join the folder path with the file name
        filePath = os.path.join(currentPath, fileName)
        df = pd.read_csv(filePath, dtype=str)
        managmentGraph(df,fileName,targetFolder)


# Main function to execute the program
def main():
    experimentName = getParameters()
    dataFolder, targetFolder = generateDynamicPaths(experimentName)
    readFolderFiles(dataFolder, targetFolder)


if __name__ == "__main__":
    main()
