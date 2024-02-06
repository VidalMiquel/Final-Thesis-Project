from decimal import DivisionByZero
import sys
import os
import json
import pandas as pd


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
    dataFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "SecondStage", "MiddleFiles"
    )
    targetFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "SecondStage", "TargetFiles"
    )
    if not os.path.exists(targetFolder):
        print(
            f"The folder {targetFolder} does not exist for experiment {experimentName}."
        )
        sys.exit(1)

    return dataFolder, targetFolder


# Function to filter data based on possession team
def filterFileByPossessionTeam(data, nameClub):
    # Filter rows based on conditions
    dataTeam = data[data["possession_team"].apply(lambda x: (x)["name"] == nameClub)]
    #dataTeamPass = dataTeam[dataTeam["type"].apply(lambda x: (x)["id"] == 30)]
   
    # Check if 'dataTeam' is not empty before proceeding
    if not dataTeam.empty:
        return dataTeam
    else:
        return None


# Function to save filtered data to a file
def saveFilteredFile(data, targetFolder, fileName):
    # Check if the segment is not empty before saving
    if not data.empty:
        # File name in the format Football_day_n_m
        newFileName = changeFilenames(fileName)
        filePath = os.path.join(targetFolder, newFileName)
        try:
            data.to_json(filePath, orient="records")
            #print(f"File stored at: {filePath}")
        except Exception as e:
            print(f"Error while saving the file: {e}")
        #print(f"File '{newFileName}' generated successfully.")
    else:
        #print(data)
        print(f"The file is empty, no file will be generated: ", fileName)


# Function to read files in a folder and process them
def readFolderFiles(currentPath, targetFolder, nameClub):
    # Check if the folder exists
    if not os.path.isdir(currentPath):
        print(f"The folder '{currentPath}' does not exist.")
        return

    # Iterate through all the files in the folder
    for fileName in os.listdir(currentPath):
        # Join the folder path with the file name
        filePath = os.path.join(currentPath, fileName)

        try:
            with open(filePath, "r+", encoding="utf-8") as file:
                content = json.load(file)
                dFrame = pd.DataFrame(content)
                
                filteredData = filterFileByPossessionTeam(dFrame, nameClub)
                saveFilteredFile(filteredData, targetFolder, fileName)
        except OSError as e:
            print(f"Error while reading the file '{fileName}': {e}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in '{fileName}': {e}")


# Function to change file names to a new format
def changeFilenames(fileName):
    # Check if the file name follows the pattern "Football_day_{jornada_value}_{i+1}.json"   
    if fileName.endswith(".json"):
            parts = fileName.split("_")
            if len(parts) == 3 and parts[2] == "footballDay.json":
                newFileName = f"{parts[0]}_{parts[1]}_footballDayFiltered.json"
                return newFileName
    else:
        print("The file name does not follow the expected pattern.")
        return None


# Main function to execute the program
def main():
    experimentName, clubName = getParameters()
    dataFolder, targetFolder = generateDynamicPaths(experimentName)
    readFolderFiles(dataFolder, targetFolder, clubName)


if __name__ == "__main__":
    main()
