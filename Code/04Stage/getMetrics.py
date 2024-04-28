# saveMetrics.py

import sys
import os
import networkx as nx
import pickle
import pandas as pd


individualNetworkMetrics = {
    'inDegree_players': {},
    'outDegree_players': {},
    'clustering_coefficients': {},
    'betweenness_centralities': {},
    'closeness_centralities': {},
    'eigenvector_centrality': {},
    'eccentricity': {}
}

globalNetworkMetrics = {
    'average_clustering': {},
    'density': {},
    #'global_efficiency': {},
    'diameter': {}
}

# Function to get command-line parameters
def getParameters():
    if len(sys.argv) == 3:
        return sys.argv[1], sys.argv[2]
    else:
        print("Exactly two values must be provided as arguments.")
        sys.exit(1)

# Function to generate dynamic paths for data and target folders
def generateDynamicPaths(experimentName, clubName):
    currentDir = os.path.abspath(
        os.path.dirname(__file__)
    )  # Get the current directory of the script

    dataFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "04Stage", "Graphs" , "diGraphs"
    )

    targetFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "04Stage", "Metrics"
    )
    
    metadataFile = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "03Stage", f"finalMetadata{clubName}.csv"
    )
    if not os.path.exists(targetFolder):
        print(
            f"The folder {targetFolder} does not exist for experiment {experimentName}."
        )
        sys.exit(1)

    return metadataFile, dataFolder, targetFolder

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


def readMetatadaFile(metadataFolder):
    try:
        dfScore = pd.read_csv(metadataFolder)
        return dfScore
    except FileNotFoundError:
        print(f"Path not found: '{metadataFolder}'.")
        return None
    except nx.NetworkXError as e:
        print(f"Path not found: '{metadataFolder}'.")
        return None
    


'''
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
'''
'''
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
'''    

   


def generatePath(targetPath, fileName):
    try:
        outputFilePath = os.path.join(targetPath, fileName)
        return outputFilePath
    except Exception as e:
        print("Error occurred while generating path:", str(e))
        return None

def saveMetrics(targetFolder, type, dicty):
    try:
        with open(f'{targetFolder}/{type}/{type}networkMetrics.pkl', 'wb') as f:
            pickle.dump(dicty, f)
        print("Metrics saved successfully.")
    except Exception as e:
        print("Error occurred while saving metrics:", str(e))

def inicializeGlobalNetworkMetrics(score, graph):
    # Initialize dictionaries for metrics if they don't exist
        if score not in globalNetworkMetrics['average_clustering']:
            globalNetworkMetrics['average_clustering'][score] = []
        if score not in globalNetworkMetrics['density']:
            globalNetworkMetrics['density'][score] = []
        #if score not in network_metrics['global_efficiency']:
            #network_metrics['global_efficiency'][score] = {}
        if nx.is_strongly_connected(graph):   
            if score not in globalNetworkMetrics['diameter']:
                globalNetworkMetrics['diameter'][score] = []
                
def initializeIndividualNetworkMetrics(score, graph):
    # Initialize dictionaries for metrics if they don't exist
        if score not in individualNetworkMetrics['inDegree_players']:
            individualNetworkMetrics['inDegree_players'][score] = {}
        if score not in individualNetworkMetrics['outDegree_players']:
            individualNetworkMetrics['outDegree_players'][score] = {}
        if score not in individualNetworkMetrics['clustering_coefficients']:
            individualNetworkMetrics['clustering_coefficients'][score] = {}
        if score not in individualNetworkMetrics['betweenness_centralities']:
            individualNetworkMetrics['betweenness_centralities'][score] = {}
        if score not in individualNetworkMetrics['closeness_centralities']:
            individualNetworkMetrics['closeness_centralities'][score] = {}
        if nx.is_strongly_connected(graph):   
            if score not in individualNetworkMetrics['eigenvector_centrality']:
                individualNetworkMetrics['eigenvector_centrality'][score] = {}
            if score not in individualNetworkMetrics['eccentricity']:
                individualNetworkMetrics['eccentricity'][score] = {}
 
def getScore(fileName):
    parts = fileName.split("_")
    if len(parts) == 4:
        pass
    elif len(parts) == 5 :
        return f"{parts[2]}_{parts[3]}"

def getGlobalMetrics(graph, score):
    # Calculate clustering coefficient and store
        average_clustering = nx.average_clustering(graph)
        globalNetworkMetrics['average_clustering'][score].append(average_clustering)
        
        #Calculate betweenness centrality and store
        density = nx.density(graph)
        globalNetworkMetrics['density'][score].append(density)
        
        #Calculate closeness centrality and store
        #global_efficiency = nx.local_efficiency(graph)
        #network_metrics['global_efficiency'][score]= global_efficiency
            
        if nx.is_strongly_connected(graph):   
            #Calcualte eccentricity and store
            diameter = nx.diameter(graph)
            globalNetworkMetrics["diameter"][score].append(diameter)
    
def getIndividualMetrics(graph, score):
     for node in graph.nodes():
            # Calculate in-degree and append to inDegree_players dictionary
            in_degree = graph.in_degree(node)
            if node not in individualNetworkMetrics['inDegree_players'][score]:
                individualNetworkMetrics['inDegree_players'][score][node] = []
            individualNetworkMetrics['inDegree_players'][score][node].append(in_degree)
            
            # Calculate out-degree and append to outDegree_players dictionary
            out_degree = graph.out_degree(node)
            if node not in individualNetworkMetrics['outDegree_players'][score]:
                individualNetworkMetrics['outDegree_players'][score][node] = []
            individualNetworkMetrics['outDegree_players'][score][node].append(out_degree)
            
            # Calculate clustering coefficient and store
            clustering_coefficient = nx.clustering(graph, node)
            individualNetworkMetrics['clustering_coefficients'][score][node] = clustering_coefficient
            
            # Calculate betweenness centrality and store
            betweenness_centrality = nx.betweenness_centrality(graph)[node]
            individualNetworkMetrics['betweenness_centralities'][score][node] = betweenness_centrality
            
            # Calculate closeness centrality and store
            closeness_centrality = nx.closeness_centrality(graph)[node]
            individualNetworkMetrics['closeness_centralities'][score][node] = closeness_centrality
            
            if nx.is_strongly_connected(graph):   
                #Calcualte eccentricity and store
                eccentricity = nx.eccentricity(graph)[node]
                individualNetworkMetrics["eccentricity"][score][node] = eccentricity
                
                #Calcualte eccentricity and store
                eigenvector = nx.eigenvector_centrality(graph)[node]
                individualNetworkMetrics["eigenvector_centrality"][score][node] = eigenvector

def manageMetrics(dataFolder, scores):
    
    if not os.path.isdir(dataFolder):
        print(f"The folder '{dataFolder}' does not exist.")
        return

    # Iterate through all the files in the folder
    for fileName in os.listdir(dataFolder):
        # Join the folder path with the file name
        graph = readGraph(dataFolder, fileName)
        score = getScore(fileName)
        if score in scores:
            initializeIndividualNetworkMetrics(score, graph)
            inicializeGlobalNetworkMetrics(score,graph)
            getIndividualMetrics(graph, score)
            getGlobalMetrics(graph, score)
            
    
    


def main():
    experimentName, clubName = getParameters()
    metadataFolder, dataFolder, targetFolder = generateDynamicPaths(experimentName, clubName)
    metadataFile = readMetatadaFile(metadataFolder)
    scores = metadataFile["Score"].unique()
    manageMetrics(dataFolder, scores)
    saveMetrics(targetFolder, "Individual", individualNetworkMetrics)
    saveMetrics(targetFolder, "Global", globalNetworkMetrics)
    
if __name__ == "__main__":
    main()