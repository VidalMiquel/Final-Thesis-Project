# saveMetrics.py

import sys
import os
import networkx as nx
import pickle
import matplotlib.pyplot as plt

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
        currentDir, "..", "..", "Data", experimentName, "04Stage", "Metrics"
    )

    targetFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "04Stage", "Graphics"
    )

    if not os.path.exists(targetFolder):
        print(
            f"The folder {targetFolder} does not exist for experiment {experimentName}."
        )
        sys.exit(1)

    return dataFolder, targetFolder

def readFileMetrics(dataFolder, fileName):
    try:
        filePath = os.path.join(dataFolder, fileName)
        with open(filePath, "rb") as f:
            deserializedFile = pickle.load(f)
        return deserializedFile
    except FileNotFoundError:
        print(f"File '{fileName}' not found in '{dataFolder}'.")
        return None
    except nx.NetworkXError as e:
        print(f"Error reading graph from '{filePath}': {e}")
        return None

# Function to change file names to a new format
def changeFilenames(fileName, final):
    # Check if the file name follows the pattern "Football_day_{jornada_value}_{i+1}.json"   
    if fileName.endswith(".pkl"):
        parts = fileName.split("_")
        if len(parts) == 4:
            newFileName = f"{parts[0]}_{parts[1]}_{parts[2]}__{final}"
            return newFileName
        elif len(parts) == 5:
            newFileName = f"{parts[0]}_{parts[1]}_{parts[2]}_{parts[3]}_{final}"
            return newFileName
        else:
            print("The file name does not follow the expected pattern.")
            return None
    else:
        print("The file name does not have a CSV extension.")
        return None
    
   

def generatePath(targetPath, fileName):
    try:
        outputFilePath = os.path.join(targetPath, fileName)
        return outputFilePath
    except Exception as e:
        print("Error occurred while generating path:", str(e))
        return None

def finalPath(path, name):
    combinedPath = os.path.join(path, name)
    return combinedPath

def finalPath(path, filename):
    return os.path.join(path, filename)

def saveBoxplot(fig, path):
    fig.savefig(path)
    plt.close()  # Close the plot to free up memory

def plotDegreeDistribution(dictionary, fileName, targetFolder):
    newFileName = changeFilenames(fileName, "DegreeDistribution.pdf")
    path = generatePath(targetFolder, newFileName)
    # Prepare data for plotting
    in_degrees = list(dictionary.get('inDegree', {}).values())
    out_degrees = list(dictionary.get('outDegree', {}).values())

    # Create boxplot
    fig, ax = plt.subplots()
    ax.boxplot([in_degrees, out_degrees], labels=['In-Degree', 'Out-Degree'])
    ax.set_title('In-Degree vs Out-Degree Boxplot')
    ax.set_xlabel('Degree Type')
    ax.set_ylabel('Degree Value')

    saveBoxplot(fig, path)
    
    
    
def getGraphics(dictionary, fileName, targetFolder):

    plotDegreeDistribution(dictionary,fileName, targetFolder)
    
def manageGraphics(dataFolder, targetFolder):
    
    if not os.path.isdir(dataFolder):
        print(f"The folder '{dataFolder}' does not exist.")
        return

    # Iterate through all the files in the folder
    for fileName in os.listdir(dataFolder):
        # Join the folder path with the file name
        dictionary = readFileMetrics(dataFolder, fileName)
        getGraphics(dictionary, fileName, targetFolder)
        
def main():
    experimentName = getParameters()
    dataFolder, targetFolder = generateDynamicPaths(experimentName)
    manageGraphics(dataFolder, targetFolder)
    
if __name__ == "__main__":
    main()