# saveMetrics.py

import sys
import os
import networkx as nx
import pickle
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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

    playersFilePath = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "04Stage", "playersList.pkl"
    )
    
    individualMetricPath = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "05Stage", "Metrics", "Classified", "Individual", "classifiedIndividualnetworkMetrics.pkl"
    )
    
    globalMetricPath = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "05Stage", "Metrics", "Raw", "Global", "GlobalnetworkMetrics.pkl"
    )

    targetFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "06Stage", "Tables"
    )

    if not os.path.exists(targetFolder):
        print(
            f"The folder {targetFolder} does not exist for experiment {experimentName}."
        )
        sys.exit(1)

    return playersFilePath, individualMetricPath, globalMetricPath, targetFolder

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
    dfNoBlank = dfNoNan.replace(" ", float('NaN'))  # Replace blank spaces with 0

    # Calculate mean, standard deviation, and count
    meanValues = dfNoBlank.mean(axis=1).round(2)
    stdValues = dfNoBlank.std(axis=1).round(2)
    countValues = dfNoBlank.count(axis=1)

    return meanValues, stdValues, countValues
    
def processAndGenerateMetrics(dfScore, deserializedFile, targetPath, mode):
    try:
        if mode == "individual":
            
            for score in dfScore["Score"].unique():
                metricsTable = pd.DataFrame()
                element_values = []
                for element in deserializedFile:
                    if score in deserializedFile[element]:
                        if not element in element_values:
                            element_values.append(element)
                        df = pd.DataFrame.from_dict(deserializedFile[element][score], orient='index')
                        metricsTable = pd.concat([metricsTable, df], axis=1)
                multi_index = pd.MultiIndex.from_product([element_values, ['Mean', 'Std', 'Count', 'Class']], names=[None, None])
                metricsTable.columns = multi_index
                metricsTable.fillna(0, inplace=True)
                metricsTable.to_pickle(f"{targetPath}/Score/Individual/{score}_individualMetrics.pkl")
        elif mode == "global":
            element_values = []
            metricsTable = pd.DataFrame()
            for element in deserializedFile:
                if not element in element_values:
                    element_values.append(element)
                df = pd.DataFrame.from_dict(deserializedFile[element], orient='index')
                meanValues, stdValues, countValues = calculateMetrics(df)
                metricsTable = pd.concat([metricsTable, meanValues.rename('Mean'), stdValues.rename('Std'), countValues.rename('Count')], axis=1)
            multi_index = pd.MultiIndex.from_product([element_values, ['Mean', 'Std', 'Count']], names=[None, None])
            metricsTable.columns = multi_index
            metricsTable.fillna(0, inplace=True)
            metricsTable.to_pickle(f"{targetPath}/Score/Global/globalMetrics.pkl")
        elif mode == "player":
            element_values = []
            scoreMetrics = {}

            for key in dfScore.keys():
                previousMetricsTable = pd.DataFrame()
                metricsTable = pd.DataFrame()
                for element in deserializedFile:
                    if not element in element_values:
                        element_values.append(element)
                    for score in deserializedFile[element]:
                        if score in deserializedFile[element]:
                            allValues = []
                            if str(key) in deserializedFile[element][score].keys():
                                values = deserializedFile[element][score][str(key)]
                                if values:           
                                    # Create or update dictionary entry for the score
                                    if score not in scoreMetrics:
                                        scoreMetrics[score] = {'Mean': values[0], 'Std': values[1], 'Count': values[2], 'Class': values[3]}
                                    else:
                                        scoreMetrics[score]['Mean'] = values[0]
                                        scoreMetrics[score]['Std'] = values[1]
                                        scoreMetrics[score]['Count'] = values[2]
                                        scoreMetrics[score]['Class'] = values[3]
                                else:
                                    if score not in scoreMetrics:
                                        scoreMetrics[score] = {'Mean': 0, 'Std': 0, 'Count': 0, 'Class':0}
                                    else:
                                        scoreMetrics[score]['Mean'] = 0
                                        scoreMetrics[score]['Std'] = 0
                                        scoreMetrics[score]['Count'] = 0
                                        scoreMetrics[score]['Class'] = 0
                            else:
                                if score not in scoreMetrics:
                                    scoreMetrics[score] = {'Mean': 0, 'Std': 0, 'Count': 0, 'Class': 0}
                                else:
                                    scoreMetrics[score]['Mean'] = 0
                                    scoreMetrics[score]['Std'] = 0
                                    scoreMetrics[score]['Count'] = 0
                                    scoreMetrics[score]['Class'] = 0

                    previousMetricsTable = pd.DataFrame.from_dict(scoreMetrics, orient='index')
                    metricsTable = pd.concat([metricsTable, previousMetricsTable], axis = 1) 
                metricsTable.columns.name = None
                multi_index = pd.MultiIndex.from_product([element_values, ['Mean', 'Std', 'Count','Class']], names=[None, None])
                metricsTable.columns = multi_index
                metricsTable.fillna(0, inplace=True)
                metricsTable.to_pickle(f"{targetPath}/Player/{key}_individualMetrics.pkl")
        else:
            raise ValueError("Invalid mode. Please choose 'individual' or 'global'.")
    except Exception as e:
        print("An error occurred:", str(e))
        
def main():
    experimentName, clubName = getParameters()
    metatadaPath = getMetadataPath(experimentName, clubName)
    metadataFile = loadMetadataFile(metatadaPath)
    playersFilePath, individMetricsPath, globalMetricPath, targetFolder = generateDynamicPaths(experimentName)
    dictyIndividual = readSerializableFile(individMetricsPath)
    dictyGlobal = readSerializableFile(globalMetricPath)
    players = readSerializableFile(playersFilePath)
    processAndGenerateMetrics(metadataFile, dictyIndividual, targetFolder, "individual")
    processAndGenerateMetrics(metadataFile, dictyGlobal, targetFolder, "global")
    processAndGenerateMetrics(players, dictyIndividual, targetFolder, "player")

    
    
if __name__ == "__main__":
    main()