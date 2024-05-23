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

    dataFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "05Stage", "Tables", "Player"
    )
    
    targetFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "06Stage", "Graphics"
    )

    if not os.path.exists(targetFolder):
        print(
            f"The folder {targetFolder} does not exist for experiment {experimentName}."
        )
        sys.exit(1)

    return  dataFolder, targetFolder

def getScatterPlot(targetFolder, df, metric, idPlayer):
    plt.figure(figsize=(12,8 ))
    sns.scatterplot(x=df.index, y=df[(f"{metric}","Class")], color='blue')

    # Adding titles and labels
    plt.title(f'Player {idPlayer} - Metric:{metric}')
    plt.xlabel('Scores')
    plt.ylabel('Classify')

    # Displaying the plot
    plt.grid(False)
    plt.savefig(f"{targetFolder}/{idPlayer}_{metric}.png")  
    plt.close()


def getIdPlayer(filename):
    parts = filename.split('_')
    return parts[0]

def generateGraphics(targetFolder, df, idPlayer):
    headers = set(header[0] for header in df.columns)
    for header in headers:
        categories = ['excellent', 'good', 'medium', 'bad', 'worst']
        cat_type = pd.CategoricalDtype(categories=categories, ordered=True)
        df[(f"{header}", 'Class')] = df[(f"{header}", 'Class')].astype(cat_type)
        getScatterPlot(targetFolder, df,header, idPlayer)
        
def readDirectory(path, targetFolder):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        
        # Check if the current path is a file
        if os.path.isfile(file_path):
            # Attempt to deserialize the file
            try:
                with open(file_path, 'rb') as file:
                    obj = pickle.load(file)
                    idPlayer = getIdPlayer(filename)
                    generateGraphics(targetFolder, obj, idPlayer)
            except Exception as e:
                print(f"Failed to read {file_path}: {e}")
        


def main():
    experimentName = getParameters()
    dataFolder, targetFolder = generateDynamicPaths(experimentName)
    readDirectory(dataFolder, targetFolder)

    
    
if __name__ == "__main__":
    main()