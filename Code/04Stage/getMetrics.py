# saveMetrics.py

import sys
import os
import networkx as nx
import pickle

total = []
# Function to get command-line parameters
def getParameters():
    if len(sys.argv) == 2:
        return sys.argv[1]
    else:
        print("Exactly two values must be provided as arguments.")
        sys.exit(1)

# Function to generate dynamic paths for data and target folders
def generateDynamicPaths(experimentName):
    currentDir = os.path.abspath(
        os.path.dirname(__file__)
    )  # Get the current directory of the script

    dataFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "04Stage", "Graphs" , "diGraphs"
    )

    targetFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "04Stage", "Metrics"
    )

    if not os.path.exists(targetFolder):
        print(
            f"The folder {targetFolder} does not exist for experiment {experimentName}."
        )
        sys.exit(1)

    return dataFolder, targetFolder

def readGraph(dataFolder, fileName):
    try:
        filePath = os.path.join(dataFolder, fileName)
        graph = nx.read_gexf(filePath)
        return graph
    except FileNotFoundError:
        print(f"File '{fileName}' not found in '{dataFolder}'.")
        return None
    except nx.NetworkXError as e:
        print(f"Error reading graph from '{filePath}': {e}")
        return None

# Function to change file names to a new format
def changeFilenames(fileName):
    # Check if the file name follows the pattern "Football_day_{jornada_value}_{i+1}.json"   
    if fileName.endswith(".gexf"):
        parts = fileName.split("_")
        if len(parts) == 4  and parts[3] == "diGraph.gexf":
            newFileName = f"{parts[0]}_{parts[1]}_{parts[2]}_Graph.pkl"
            return newFileName, parts[2]
        elif len(parts) == 5  and parts[4] == "diGraph.gexf":
            newFileName = f"{parts[0]}_{parts[1]}_{parts[2]}_{parts[3]}_Graph.pkl"
            return newFileName, f"{parts[2]}_{parts[3]}"
        else:
            print("The file name does not follow the expected pattern.")
            return None
    else:
        print("The file name does not have a gexf extension.")
        return None
    
def getDegree(G, nodeMetrics):
    nodes = list(G.nodes())

    # Calculate in-degree and out-degree for each node using list comprehensions
    inDegree = list(dict(G.in_degree()).values())
    outDegree = list(dict(G.out_degree()).values())

    # Combine node IDs with their respective in-degree and out-degree using zip
    nodeMetrics['inDegree'] = dict(zip(nodes, inDegree))
    nodeMetrics['outDegree'] = dict(zip(nodes, outDegree))

def getClustering(G, nodeMetrics):
    nodeMetrics['clustering'] = nx.clustering(G)
    nodeMetrics['averageClustering'] = nx.average_clustering(G)
    
def getCloseness(G, nodeMetrics):
    nodeMetrics['closness'] = nx.closeness_centrality(G)

def getEfficiency(G,nodeMetrics):
    nodeMetrics['globalEfficiency'] = nx.global_efficiency(G)
    
def getCommunities(G, nodeMetrics):
    nodeMetrics['communityLouvian'] = nx.community.louvain_communities(G)
    nodeMetrics['communityGreedy'] = nx.algorithms.community.greedy_modularity_communities(G)
    
def getBetweenness(G, nodeMetrics):
    nodeMetrics['betweenness'] = nx.betweenness_centrality(G)

def getDensity(G, nodeMetrics):
    nodeMetrics['density'] = nx.density(G)
   
def getDiamater(G, nodeMetrics):
    nodeMetrics['diamater'] = nx.diameter(G)

def getEccentricity(G, nodeMetrics):
    nodeMetrics['eccentricity'] = nx.eccentricity(G)

def getEigenvector(G, nodeMetrics):
    nodeMetrics['eigenvector'] = nx.eigenvector_centrality(G) 

    
def getMetrics(G, nodeMetrics):
    getDegree(G, nodeMetrics)
    getClustering(G, nodeMetrics)
    getCloseness(G, nodeMetrics)
    getCommunities(G, nodeMetrics)
    getBetweenness(G, nodeMetrics)
    getDensity(G, nodeMetrics)
    if nx.is_strongly_connected(G):
        getDiamater(G, nodeMetrics)
        getEccentricity(G, nodeMetrics)
        getEigenvector(G, nodeMetrics)
   
def saveMetrics(path, nodeMetrics):
    try:
        with open(path, 'wb') as f:
            pickle.dump(nodeMetrics, f)
    except Exception as e:
        print("Error occurred while saving metrics:", str(e))

def generatePath(targetPath, fileName):
    try:
        outputFilePath = os.path.join(targetPath, fileName)
        return outputFilePath
    except Exception as e:
        print("Error occurred while generating path:", str(e))
        return None

def saveTotal(targetFolder):
    try:
        with open(f'{targetFolder}/allMetrics.pkl', 'wb') as f:
            pickle.dump(total, f)
        print("Metrics saved successfully.")
    except Exception as e:
        print("Error occurred while saving metrics:", str(e))
        
def manageMetrics(dataFolder, targetFolder):
    
    if not os.path.isdir(dataFolder):
        print(f"The folder '{dataFolder}' does not exist.")
        return

    # Iterate through all the files in the folder
    for fileName in os.listdir(dataFolder):
        # Join the folder path with the file name
        graph = readGraph(dataFolder, fileName)
        newFileName, score = changeFilenames(fileName)
        nodeMetrics = {}  # Create a new dictionary for each file
        getMetrics(graph, nodeMetrics)
        nodeMetrics["score"] = score
        total.append(nodeMetrics)
        #path = generatePath(targetFolder, newFileName)
        #saveMetrics(path, nodeMetrics)


    saveTotal(targetFolder)


def main():
    experimentName = getParameters()
    dataFolder, targetFolder = generateDynamicPaths(experimentName)
    manageMetrics(dataFolder, targetFolder)
    
if __name__ == "__main__":
    main()