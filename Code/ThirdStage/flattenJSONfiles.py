from operator import index
import sys
import os
import json
import pandas as pd
from flatten_json import flatten


# Function to get command-line parameters
def getParameters():
    if len(sys.argv) == 2:
        return sys.argv[1]
    else:
        print("Exactly one value must be provided as arguments.")
        sys.exit(1)


# Function to generate dynamic paths for data and target folders
def generateDynamicPaths(experimentName):
    currentDir = os.path.abspath(
        os.path.dirname(__file__)
    )  # Get the current directory of the script
    dataFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "SecondStage", "Target_files"
    )
    targetFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "ThirdStage", "Middle_files"
    )

    if not os.path.exists(targetFolder):
        print(
            f"The folder {targetFolder} does not exist for experiment {experimentName}."
        )
        sys.exit(1)

    return dataFolder, targetFolder


# Function to save filtered data to a file
def saveFilteredFile(data, targetFolder, fileName):
    # Check if the segment is not empty before saving

    if not data.empty:
        # File name in the format Football_day_n_m
        newFileName = changeFilenames(fileName)
        filePath = os.path.join(targetFolder, newFileName)
        try:
            data.to_csv(filePath, index=False, encoding="utf-8-sig")
            # print(f"File stored at: {filePath}")
        except Exception as e:
            print(f"Error while saving the file: {e}")
        # print(f"File '{newFileName}' generated successfully.")
    else:
        # print(data)
        print(f"The file is empty, no file will be generated: ", fileName)


# Function to read files in a folder and process them
def readFolderFiles(currentPath, targetFolder):
    # Check if the folder exists
    if not os.path.isdir(currentPath):
        print(f"The folder '{currentPath}' does not exist.")
        return

    # Iterate through all the files in the folder
    for fileName in os.listdir(currentPath):
        # Join the folder path with the file name
        filePath = os.path.join(currentPath, fileName)

        try:
            with open(filePath, "r") as file:
                content = json.load(file)
                df = pd.DataFrame([flatten(d) for d in content])
                saveFilteredFile(df, targetFolder, fileName)
        except OSError as e:
            print(f"Error while reading the file '{fileName}': {e}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in '{fileName}': {e}")

    
# Function to change file names to a new format
def changeFilenames(fileName):
    # Check if the file name follows the pattern "Football_day_{jornada_value}_{i+1}.json"   
    if fileName.endswith(".json"):
            parts = fileName.split("_")
            if len(parts) == 3 and parts[2] == "footballDayFiltered.json":
                newFileName = f"{parts[0]}_{parts[1]}_footballDayFlattened.csv"
                return newFileName
    else:
        print("The file name does not follow the expected pattern.")
        return None


# Main function to execute the program
def main():
    experimentName = getParameters()
    dataFolder, targetFolder = generateDynamicPaths(experimentName)
    readFolderFiles(dataFolder, targetFolder)


if __name__ == "__main__":
    main()
