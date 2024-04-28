# saveMetrics.py

import sys
import os
import networkx as nx
import pickle
import matplotlib.pyplot as plt
import pandas as pd

nodeMetrics = {}

# Function to get command-line parameters
def getParameters():
    if len(sys.argv) == 3:
        return sys.argv[1], sys.argv[2]
    else:
        print("Exactly two values must be provided as arguments.")
        sys.exit(1)

# Function to generate dynamic paths for data and target folders
def generateDynamicPaths(experimentName):
    currentDir = os.path.abspath(
        os.path.dirname(__file__)
    )  # Get the current directory of the script

    individualMetricPath = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "04Stage", "Metrics", "Individual", "IndividualnetworkMetrics.pkl"
    )
    
    globalMetricPath = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "04Stage", "Metrics", "Global", "GlobalnetworkMetrics.pkl"
    )

    targetFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "05Stage", "Tables"
    )

    if not os.path.exists(targetFolder):
        print(
            f"The folder {targetFolder} does not exist for experiment {experimentName}."
        )
        sys.exit(1)

    return individualMetricPath, globalMetricPath, targetFolder

def readFileMetrics(filePath):
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
    
def getMetadataPath(experimentName, name):
    currentDir = os.path.abspath(os.path.dirname(__file__)
    )  # Get the current directory of the script

    metadataPath = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "03Stage", f"finalMetadata{name}.csv"
    )
    return metadataPath

def loadMetadataFile(path):
    try:
        # Open the CSV file
        # Create a CSV reader object
        dfScore = pd.read_csv(path)
        return dfScore
    except FileNotFoundError:
        print("The file does not exist.")
    except Exception as e:
        print("An error occurred:", e)
    
def calculateMetrics(data):
    dfNoNan = data.fillna(" ")
    dfNoBlank = dfNoNan.replace(" ", float('nan'))  # Replace blank spaces with NaN

    # Calculate mean, standard deviation, and count
    meanValues = dfNoBlank.mean(axis=1).round(2)
    stdValues = dfNoBlank.std(axis=1).round(2)
    countValues = dfNoBlank.count(axis=1)

    return meanValues, stdValues, countValues

def processAndGenerateMetrics(dfScore, deserializedFile, targetPath, mode):
    

    if mode == "individual":
        for score in dfScore["Score"].unique():
            metricsTable = pd.DataFrame()
            for element in deserializedFile:
                if score in deserializedFile[element]:
                    df = pd.DataFrame.from_dict(deserializedFile[element][score], orient='index')
                    meanValues, stdValues, countValues = calculateMetrics(df)
                    metricsTable = pd.concat([metricsTable, meanValues.rename('Mean'), stdValues.rename('Std'), countValues.rename('Count')], axis=1)
            metricsTable.to_csv(f"{targetPath}/Individual/{score}_individualMetrics.csv", index=True)
    
    elif mode == "global":
        metricsTable = pd.DataFrame()
        for element in deserializedFile:
            df = pd.DataFrame.from_dict(deserializedFile[element], orient='index')
            meanValues, stdValues, countValues = calculateMetrics(df)
            metricsTable = pd.concat([metricsTable, meanValues.rename('Mean'), stdValues.rename('Std'), countValues.rename('Count')], axis=1)

        metricsTable.to_csv(f"{targetPath}/Global/globalMetrics.csv", index=True)
    
    else:
        raise ValueError("Invalid mode. Please choose 'individual' or 'global'.")

        
        
def main():
    experimentName, clubName = getParameters()
    metatadaPath = getMetadataPath(experimentName, clubName)
    metadataFile = loadMetadataFile(metatadaPath)
    individMetricsPath, globalMetricPath, targetFolder = generateDynamicPaths(experimentName)
    dictyIndividual = readFileMetrics(individMetricsPath)
    dictyGlobal = readFileMetrics(globalMetricPath)
    processAndGenerateMetrics(metadataFile, dictyIndividual, targetFolder, "individual")
    processAndGenerateMetrics(metadataFile, dictyGlobal, targetFolder, "global")
    
if __name__ == "__main__":
    main()