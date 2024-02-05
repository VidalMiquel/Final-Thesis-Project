import sys
import os
import csv
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
    # print(currentDir)
    dataFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "ThirdStage", "Middle_files"
    )
    # print(dataFolder)
    targetFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "ThirdStage", "Target_files"
    )
    # print(targetFolder)

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
        # print(newFileName)
        filePath = os.path.join(targetFolder, newFileName)
        try:
            data.to_csv(filePath, index=False, encoding="utf-8-sig")
            # print(f"File stored at: {filePath}")
        except Exception as e:
            print(f"Error while saving the file: {e}")
        # print(f"File '{newFileName}' generated successfully.")
    else:
        print(f"The file is empty, no file will be generated: ", fileName)


# Function to read files in a folder and process them
def readFolderFiles(currentPath, targetFolder, clubName):
    # Check if the folder exists
    if not os.path.isdir(currentPath):
        print(f"The folder '{currentPath}' does not exist.")
        return

    # Iterate through all the files in the folder
    for fileName in os.listdir(currentPath):
        # Join the folder path with the file name
        filePath = os.path.join(currentPath, fileName)
        df = pd.read_csv(filePath, dtype=str)
        filteredData = filterByPasses(df, clubName)
        saveFilteredFile(filteredData, targetFolder, fileName)


def changeFilenames(fileName):
    # Check if the file name follows the pattern "footballDayFiltered_{jornada_value}_{i_value}.json"
    if fileName.startswith("footballDayFlattened_") and fileName.endswith(".csv"):
        parts = fileName.split("_")
        jornadaValue = parts[1]
        iValue = parts[2].split(".")[0]
        # New file name
        newFileName = f"footballDayPasses_{jornadaValue}_{iValue}.csv"
        return newFileName
    else:
        print("The file name does not follow the expected pattern.", fileName)
        return None


def filterByPasses(dfRaw, clubName):
    finalDf = pd.DataFrame()
    # List of columns you want to add to the final DataFrame. PROBLEMATIC COLUMN IS: PASS_OUTCOME_NAME
    columns_to_add = [
        "index",
        "period",
        "minute",
        "second",
        "type_id",
        "team_name",
        "type_name",
        "possession",
        "play_pattern_name",
        "player_id",
        "player_name",
        "position_id",
        "position_name",
        "location_0",
        "location_1",
        "pass_recipient_id",
        "pass_recipient_name",
        "pass_length",
        "pass_height_id",
        "pass_height_name",
        "pass_end_location_0",
        "pass_end_location_1",
        "pass_body_part_name",
        "pass_outcome_name",
    ]

    # Remove NaN values
    dfNoNan = dfRaw.dropna(axis=1, how="all")
    passes = dfNoNan.loc[(dfNoNan["type_id"] == "30") & (dfNoNan["team_name"] == clubName)]
    if not passes.empty:
        # Check if each column exists in the passes DataFrame before adding it
        for col in columns_to_add:
            if col in passes.columns:
                # If the column exists in passes, add it to the final DataFrame
                finalDf[col] = passes[col]
            else:
                print(f"Column '{col}' does not exist in the passes DataFrame.")
        return finalDf
    else:
        return passes




# Main function to execute the program
def main():
    experimentName, clubName = getParameters()
    dataFolder, targetFolder = generateDynamicPaths(experimentName)
    readFolderFiles(dataFolder, targetFolder, clubName)


if __name__ == "__main__":
    main()
