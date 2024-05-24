# saveMetrics.py

import sys
import os
import pickle
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns


nodeMetrics = {}

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

    dataFolderPlayer = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "05Stage", "Tables", "Raw", "Player"
    )
    
    dataFolderScoreIndividual = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "05Stage", "Tables", "Raw", "Score", "Individual"
    )
    
    targetFolderPlayer = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "05Stage", "Tables", "Filtered", "Player"
    )
    
    targetFolderScoreIndividual = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "05Stage", "Tables", "Filtered", "Score", "Individual"
    )


    return  dataFolderPlayer, dataFolderScoreIndividual, targetFolderPlayer, targetFolderScoreIndividual



def filterTables(df):
    max_value = df[('inD', 'Count')].max()
    # Step 2: Calculate the threshold (1/4 of the maximum value)
    threshold = max_value / 4
    # Step 3: Filter the DataFrame
    filteredDf = df[df[('inD', 'Count')] >= threshold]
    return filteredDf
    #filteredDf.to_pickle(f"{targetPath}/{id}_filteredIndividualMetrics.pkl")
    
def cutTables(filteredTable):
    headers = set(header[0] for header in filteredTable.columns)
        
    #print(filteredTable)
    for header in headers:
        classifyValues = pd.cut(np.array(filteredTable[(f"{header}", "Mean")]), 5, labels=["worst", "bad", "medium", "good", "excellent"]).astype(str)
        columnClassify = pd.Series(classifyValues, index=filteredTable.index, name=(header, 'Class'))
        mean_idx = filteredTable.columns.get_loc((header, 'Count'))
        insert_position = mean_idx + 1
        filteredTable.insert(insert_position, (header, 'Class'), columnClassify)
    return filteredTable
        
def getIdFile(filename):
    parts = filename.split('_')
    if len(parts) == 2:
        return parts[0]
    else:
        return f"{parts[0]}_{parts[1]}"
  
def readDirectory(path, targetFolder):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        
        # Check if the current path is a file
        if os.path.isfile(file_path):
            # Attempt to deserialize the file
            try:
                with open(file_path, 'rb') as file:
                    obj = pickle.load(file)
                    if not obj.empty:
                        id = getIdFile(filename)
                        filteredDF =filterTables(obj)
                        finalTable = cutTables(filteredDF)
                        finalTable.to_pickle(f"{targetFolder}/{id}_filteredIndividualMetrics.pkl")

            except Exception as e:
                print(f"Failed to read {file_path}: {e}")
        


def main():
    experimentName = getParameters()
    dataFolderPlayer, dataFolderScoreIndividual, targetFolderPlayer, targetFolderScoreIndividual = generateDynamicPaths(experimentName)
    #readDirectory(dataFolderPlayer, targetFolderPlayer)
    readDirectory(dataFolderScoreIndividual, targetFolderScoreIndividual)

    
    
if __name__ == "__main__":
    main()