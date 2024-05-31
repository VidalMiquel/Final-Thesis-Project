# saveMetrics.py

import os
import pickle
import sys

import networkx as nx
import pandas as pd

nodeMetrics = {}


# Function to get command-line parameters.
def getParameters():
    if len(sys.argv) == 2:
        return sys.argv[1]
    else:
        print("Exactly two values must be provided as arguments.")
        sys.exit(1)


# Function to generate dynamic paths for data and target folders.
def generateDynamicPaths(experimentName):
    currentDir = os.path.abspath(
        os.path.dirname(__file__)
    )  # Get the current directory of the script

    dataFolder = os.path.join(
        currentDir,
        "..",
        "..",
        "Data",
        experimentName,
        "05Stage",
        "Metrics",
        "Raw",
        "Individual",
        "IndividualnetworkMetrics.pkl",
    )

    targetFolder = os.path.join(
        currentDir,
        "..",
        "..",
        "Data",
        experimentName,
        "05Stage",
        "Metrics",
        "Normalized",
        "Individual",
    )

    if not os.path.exists(targetFolder):
        print(
            f"The folder {targetFolder} does not exist for experiment {experimentName}."
        )
        sys.exit(1)

    return dataFolder, targetFolder


# Read serializabel file.
def readSerializableFile(filePath):
    try:
        with open(filePath, "rb") as f:
            deserializedFile = pickle.load(f)
        return deserializedFile
    except FileNotFoundError:
        print(f"File not found in '{filePath}'.")
        return None
    except nx.NetworkXError as e:
        print(f"Error reading graph from '{filePath}': {e}")
        return None


# Save dictionary as a object.
def saveDictToPickle(dictionary, filePath):
    try:
        with open(f"{filePath}/normalizateIndividualnetworkMetrics.pkl", "wb") as f:
            pickle.dump(dictionary, f)
        # print("Dictionary saved to", filePath)
    except Exception as e:
        print("Error occurred while saving the dictionary:", str(e))


# Normalizate dict values.
def nomralizatedMetrics(file):
    finalDict = {}
    for element in file:
        concatenated_dict = {}
        for score in file[element]:
            df = pd.DataFrame.from_dict(file[element][score], orient="index")
            dfN = (df - df.min()) / (df.max() - df.min())
            dfN.set_index(df.index, inplace=True)
            a = dfN.T.to_dict(orient="list")
            concatenated_dict[score] = a
        finalDict[element] = concatenated_dict
    return finalDict


def main():
    experimentName = getParameters()
    dataFolder, targetFolder = generateDynamicPaths(experimentName)
    individualMetrics = readSerializableFile(dataFolder)
    normalizatedMetrics = nomralizatedMetrics(individualMetrics)
    saveDictToPickle(normalizatedMetrics, targetFolder)


if __name__ == "__main__":
    main()
