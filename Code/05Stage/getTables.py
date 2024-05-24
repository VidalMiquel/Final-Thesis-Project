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
        currentDir, "..", "..", "Data", experimentName, "04Stage", "Metrics", "Individual", "IndividualnetworkMetrics.pkl"
    )
    
    globalMetricPath = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "04Stage", "Metrics", "Global", "GlobalnetworkMetrics.pkl"
    )

    targetFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "05Stage", "Tables", "Raw"
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
                        meanValues, stdValues, countValues = calculateMetrics(df)
                        #classifyValues = pd.cut(np.array(meanValues), 5, labels=["worst", "bad", "medium", "good", "excellent"]).astype(str)
                        #columnClassifiy = pd.DataFrame({'Class': classifyValues}, index=meanValues.index)
                        metricsTable = pd.concat([metricsTable, meanValues.rename('Mean'), stdValues.rename('Std'), countValues.rename('Count')], axis=1)
                multi_index = pd.MultiIndex.from_product([element_values, ['Mean', 'Std', 'Count']], names=[None, None])
                metricsTable.columns = multi_index
                #metricsTable.to_csv(f"{targetPath}/Score/Individual/{score}_individualMetrics.csv", index=True)
                metricsTable.to_pickle(f"{targetPath}/Score/Individual/{score}_individualMetrics.pkl")
        elif mode == "global":
            element_values = []
            metricsTable = pd.DataFrame()
            #columnClassifiy = pd.DataFrame()
            for element in deserializedFile:
                if not element in element_values:
                    element_values.append(element)
                df = pd.DataFrame.from_dict(deserializedFile[element], orient='index')
                meanValues, stdValues, countValues = calculateMetrics(df)
                #classifyValues = pd.cut(np.array(meanValues), 5, labels=["worst", "bad", "medium", "good", "excellent"]).astype(str)
                #columnClassifiy = pd.DataFrame({'Class': classifyValues}, index=meanValues.index)
                metricsTable = pd.concat([metricsTable, meanValues.rename('Mean'), stdValues.rename('Std'), countValues.rename('Count')], axis=1)
            multi_index = pd.MultiIndex.from_product([element_values, ['Mean', 'Std', 'Count']], names=[None, None])
            metricsTable.columns = multi_index
            #metricsTable.to_csv(f"{targetPath}/Score/Global/globalMetrics.csv")
            metricsTable.to_pickle(f"{targetPath}/Score/Global/globalMetrics.pkl")
        elif mode == "player":
            scoreMetrics = {}
            element_values = []
            for key in dfScore.keys():
                previousMetricsTable = pd.DataFrame()
                metricsTable = pd.DataFrame()
                for element in deserializedFile:
                    if not element in element_values:
                        element_values.append(element)
                    for score in deserializedFile[element]:
                        #print(f"Resultat: {score}")
                        allValues = []
                        if str(key) in deserializedFile[element][score].keys():
                            values = deserializedFile[element][score][str(key)]
                            if isinstance(values, list):
                                allValues.extend(values)
                            else:
                                allValues.append(values)
                            meanValue = np.mean(values)
                            stdValue = np.std(values)
                            if isinstance(values, list):
                                countValue = len(values)
                            else:
                                countValue = 1
                            # Round the calculated values
                            meanValue = round(meanValue, 2)
                            stdValue = round(stdValue, 2)
                        
                            # Create or update dictionary entry for the score
                            if score not in scoreMetrics:
                                scoreMetrics[score] = {'Mean': meanValue, 'Std': stdValue, 'Count': countValue}
                            else:
                                scoreMetrics[score]['Mean'] = meanValue
                                scoreMetrics[score]['Std'] = stdValue
                                scoreMetrics[score]['Count'] = countValue
                        else:
                            if score not in scoreMetrics:
                                scoreMetrics[score] = {'Mean': meanValue, 'Std': stdValue, 'Count': countValue}
                            else:
                                scoreMetrics[score]['Mean'] = 0
                                scoreMetrics[score]['Std'] = 0
                                scoreMetrics[score]['Count'] = 0
                        
                        # Concatenate horizontally with the main DataFrame
                    previousMetricsTable = pd.DataFrame.from_dict(scoreMetrics, orient='index')
                    #classifyValues = pd.cut(np.array(previousMetricsTable["Mean"]), 5, labels=["worst", "bad", "medium", "good", "excellent"]).astype(str)
                    #columnClassifiy = pd.DataFrame({'Class': classifyValues}, index=previousMetricsTable["Mean"].index)
                    metricsTable = pd.concat([metricsTable, previousMetricsTable], axis = 1)                                      
                    
                metricsTable.columns.name = None
                multi_index = pd.MultiIndex.from_product([element_values, ['Mean', 'Std', 'Count']], names=[None, None])
                metricsTable.columns = multi_index
                #metricsTable.to_csv(f"{targetPath}/Player/{key}_individualMetrics.csv", index = True)
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