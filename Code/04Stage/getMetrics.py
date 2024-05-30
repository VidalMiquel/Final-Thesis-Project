import os
import pickle
import sys

import networkx as nx
import pandas as pd

# Define data strucutre for individual metrics.
individualNetworkMetrics = {
    "inD": {},
    "outD": {},
    "clust": {},
    "betw": {},
    "clos": {},
    "eigenv": {},
    "ecce": {},
}

# Define data strucutre for global metrics.
globalNetworkMetrics = {"av_clust": {}, "dty": {}, "diam": {}}


# Function to get command-line parameters.
def getParameters():
    if len(sys.argv) == 3:
        return sys.argv[1], sys.argv[2]
    else:
        print("Exactly two values must be provided as arguments.")
        sys.exit(1)


# Function to generate dynamic paths for data and target folders.
def generateDynamicPaths(experimentName, clubName):
    currentDir = os.path.abspath(
        os.path.dirname(__file__)
    )  # Get the current directory of the script

    dataFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "04Stage", "Graphs", "diGraphs"
    )

    targetFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "04Stage", "Metrics"
    )

    metadataFile = os.path.join(
        currentDir,
        "..",
        "..",
        "Data",
        experimentName,
        "03Stage",
        f"finalMetadata{clubName}.csv",
    )
    if not os.path.exists(targetFolder):
        print(
            f"The folder {targetFolder} does not exist for experiment {experimentName}."
        )
        sys.exit(1)

    return metadataFile, dataFolder, targetFolder


# Read graph.
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


# Read last version metadatas file.
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


# Generate final path from a given path and fileName.
def generatePath(targetPath, fileName):
    try:
        outputFilePath = os.path.join(targetPath, fileName)
        return outputFilePath
    except Exception as e:
        print("Error occurred while generating path:", str(e))
        return None


# Save file metrics.
def saveMetrics(targetFolder, type, dicty):
    try:
        with open(f"{targetFolder}/{type}/{type}networkMetrics.pkl", "wb") as f:
            pickle.dump(dicty, f)
    except Exception as e:
        print("Error occurred while saving metrics:", str(e))


def inicializeGlobalNetworkMetrics(score, graph):
    # Initialize dictionaries for metrics if they don't exist
    if score not in globalNetworkMetrics["av_clust"]:
        globalNetworkMetrics["av_clust"][score] = []
    if score not in globalNetworkMetrics["dty"]:
        globalNetworkMetrics["dty"][score] = []
    if nx.is_strongly_connected(graph):
        if score not in globalNetworkMetrics["diam"]:
            globalNetworkMetrics["diam"][score] = []


def initializeIndividualNetworkMetrics(score, graph):
    # Initialize dictionaries for metrics if they don't exist
    if score not in individualNetworkMetrics["inD"]:
        individualNetworkMetrics["inD"][score] = {}
    if score not in individualNetworkMetrics["outD"]:
        individualNetworkMetrics["outD"][score] = {}
    if score not in individualNetworkMetrics["clust"]:
        individualNetworkMetrics["clust"][score] = {}
    if score not in individualNetworkMetrics["betw"]:
        individualNetworkMetrics["betw"][score] = {}
    if score not in individualNetworkMetrics["clos"]:
        individualNetworkMetrics["clos"][score] = {}
    if nx.is_strongly_connected(graph):
        if score not in individualNetworkMetrics["eigenv"]:
            individualNetworkMetrics["eigenv"][score] = {}
        if score not in individualNetworkMetrics["ecce"]:
            individualNetworkMetrics["ecce"][score] = {}


# Get score from a given fileName.
def getScore(fileName):
    parts = fileName.split("_")
    if len(parts) == 4:
        pass
    elif len(parts) == 5:
        return f"{parts[2]}_{parts[3]}"


# Get global metrics for a given graph.
def getGlobalMetrics(graph, score):
    # Calculate clustering coefficient and store
    average_clustering = nx.average_clustering(graph)
    globalNetworkMetrics["av_clust"][score].append(average_clustering)

    # Calculate betweenness centrality and store
    density = nx.density(graph)
    globalNetworkMetrics["dty"][score].append(density)

    if nx.is_strongly_connected(graph):
        # Calcualte eccentricity and store
        diameter = nx.diameter(graph)
        globalNetworkMetrics["diam"][score].append(diameter)


# Get individual metrics (nodes) for a given grpah
def getIndividualMetrics(graph, score):
    for node in graph.nodes():
        # Calculate in-degree and append to inDegree_players dictionary
        in_degree = graph.in_degree(node)
        if node not in individualNetworkMetrics["inD"][score]:
            individualNetworkMetrics["inD"][score][node] = []
        individualNetworkMetrics["inD"][score][node].append(in_degree)

        # Calculate out-degree and append to outDegree_players dictionary
        out_degree = graph.out_degree(node)
        if node not in individualNetworkMetrics["outD"][score]:
            individualNetworkMetrics["outD"][score][node] = []
        individualNetworkMetrics["outD"][score][node].append(out_degree)

        # Calculate clustering coefficient and store
        clustering_coefficient = nx.clustering(graph, node)
        if node not in individualNetworkMetrics["clust"][score]:
            individualNetworkMetrics["clust"][score][node] = []
        individualNetworkMetrics["clust"][score][node].append(clustering_coefficient)

        # Calculate betweenness centrality and store
        betweenness_centrality = nx.betweenness_centrality(graph)[node]
        if node not in individualNetworkMetrics["betw"][score]:
            individualNetworkMetrics["betw"][score][node] = []
        individualNetworkMetrics["betw"][score][node].append(betweenness_centrality)

        # Calculate closeness centrality and store
        closeness_centrality = nx.closeness_centrality(graph)[node]
        if node not in individualNetworkMetrics["clos"][score]:
            individualNetworkMetrics["clos"][score][node] = []
        individualNetworkMetrics["clos"][score][node].append(closeness_centrality)

        if nx.is_strongly_connected(graph):
            # Calcualte eccentricity and store
            eccentricity = nx.eccentricity(graph)[node]
            if node not in individualNetworkMetrics["ecce"][score]:
                individualNetworkMetrics["ecce"][score][node] = []
            individualNetworkMetrics["ecce"][score][node].append(eccentricity)

            # Calcualte eccentricity and store
            eigenvector = nx.eigenvector_centrality(graph)[node]
            if node not in individualNetworkMetrics["eigenv"][score]:
                individualNetworkMetrics["eigenv"][score][node] = []
            individualNetworkMetrics["eigenv"][score][node].append(eigenvector)


# Manage getting metrics
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
            inicializeGlobalNetworkMetrics(score, graph)
            getIndividualMetrics(graph, score)
            getGlobalMetrics(graph, score)


def main():
    experimentName, clubName = getParameters()
    metadataFolder, dataFolder, targetFolder = generateDynamicPaths(
        experimentName, clubName
    )
    metadataFile = readMetatadaFile(metadataFolder)
    scores = metadataFile["Score"].unique()
    manageMetrics(dataFolder, scores)
    saveMetrics(targetFolder, "Individual", individualNetworkMetrics)
    saveMetrics(targetFolder, "Global", globalNetworkMetrics)


if __name__ == "__main__":
    main()
