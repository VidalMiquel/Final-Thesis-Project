# saveMetrics.py

import os
import pickle
import sys
import numpy as np
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
        "Normalized",
        "Individual",
        "normalizateIndividualnetworkMetrics.pkl",
    )

    targetFolder = os.path.join(
        currentDir,
        "..",
        "..",
        "Data",
        experimentName,
        "05Stage",
        "Metrics",
        "Classified",
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
        with open(f"{filePath}/classifiedIndividualnetworkMetrics.pkl", "wb") as f:
            pickle.dump(dictionary, f)
        # print("Dictionary saved to", filePath)
    except Exception as e:
        print("Error occurred while saving the dictionary:", str(e))
        

def calculateMetrics(data):
    dfNoNan = data.fillna(" ")
    dfNoBlank = dfNoNan.replace(" ", float('NaN'))  # Replace blank spaces with 0
    # Calculate mean, standard deviation, and count
    meanValues = dfNoBlank.mean(axis=1).round(2)
    stdValues = dfNoBlank.std(axis=1).round(2)
    countValues = dfNoBlank.count(axis=1)

    return meanValues, stdValues, countValues

def classifiedMetrics(file):
    finalDict = {}
    for element in file:
        concatenated_dict = {}
        for score in file[element]:
            metricsTable = pd.DataFrame()
            df = pd.DataFrame.from_dict(file[element][score], orient="index")
            meanValues, stdValues, countValues = calculateMetrics(df)  
            meanDropNa = meanValues.dropna(axis=0)
            if  not meanDropNa.empty:
                classifyValues = pd.cut(np.array(meanDropNa), 5, labels=["worst", "bad", "medium", "good", "excellent"]).astype(str)
                columnClassifiy = pd.DataFrame({'Class': classifyValues}, index=meanDropNa.index)
                metricsTable = pd.concat([metricsTable, meanDropNa.rename('Mean'), stdValues.rename('Std'), countValues.rename('Count'), columnClassifiy], axis=1)
                metricsTable.set_index(df.index, inplace=True)
                metricsTableDict = metricsTable.T.to_dict(orient="list")
                concatenated_dict[score] = metricsTableDict
        finalDict[element] = concatenated_dict
    return finalDict

def main():
    experimentName = getParameters()
    dataFolder, targetFolder = generateDynamicPaths(experimentName)
    individualMetrics = readSerializableFile(dataFolder)
    normalizatedMetrics = classifiedMetrics(individualMetrics)
    saveDictToPickle(normalizatedMetrics, targetFolder)


if __name__ == "__main__":
    main()
