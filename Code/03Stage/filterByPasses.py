import os
import sys

import pandas as pd


# Function to get command-line parameters.
def getParameters():
    if len(sys.argv) == 3:
        return sys.argv[1], sys.argv[2]
    else:
        print("Exactly two values must be provided as arguments.")
        sys.exit(1)


# Read the first metadataFiles version.
def getMetaDataFile(path, clubName):
    try:
        fileName = f"metadata{clubName}.csv"
        filePath = os.path.join(path, fileName)
        df = pd.read_csv(filePath, dtype=str)
        return df
    except FileNotFoundError:
        print(f"File not found at path: {path}")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


# Function to generate dynamic paths for data and target folders.
def generateDynamicPaths(experimentName):
    currentDir = os.path.abspath(
        os.path.dirname(__file__)
    )  # Get the current directory of the script

    dataFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "03Stage", "MiddleFiles"
    )

    targetFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "03Stage", "TargetFiles"
    )
    metaDataFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "02Stage"
    )

    if not os.path.exists(targetFolder):
        print(
            f"The folder {targetFolder} does not exist for experiment {experimentName}."
        )
        sys.exit(1)

    return dataFolder, targetFolder, metaDataFolder


# Function to save filtered data to a file.
def saveFilteredFile(data, targetFolder, fileName, metadata):
    # Check if the segment is not empty before saving

    if not data.empty:
        # File name in the format Football_day_n_m
        newFileName = changeFilenames(fileName, metadata)

        filePath = os.path.join(targetFolder, newFileName)
        try:
            data.to_csv(filePath, index=False, encoding="utf-8-sig")
            # print(f"File stored at: {filePath}")
        except Exception as e:
            print(f"Error while saving the file: {e}")

    else:
        print(fileName)
        # print(f"The file is empty, no file will be generated: ", fileName)
        pass


# Function to read files in a folder and process them
def readFolderFiles(currentPath, targetFolder, clubName, metadata):
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
        saveFilteredFile(filteredData, targetFolder, fileName, metadata)


# Function to change file names to a new format
def changeFilenames(fileName, metadata):
    # Check if the file name follows the pattern "Football_day_{jornada_value}_{i+1}.json"
    if fileName.endswith(".csv"):
        parts = fileName.split("_")
        if len(parts) == 3 and parts[2] == "footballDayFlattened.csv":
            id_value = f"{parts[0]}_{parts[1]}"
            # Filter metadata based on IdFile
            filteredMetadata = metadata[metadata["IdFiles"] == id_value]

            if not filteredMetadata.empty:
                NF = filteredMetadata["NoInformation"].values[0]

                if NF == "NF":
                    newFileName = f"{parts[0]}_{parts[1]}_{NF}_footballDayPasses.csv"
                else:
                    score = filteredMetadata["Score"].values[0]
                    newFileName = f"{parts[0]}_{parts[1]}_{score}_footballDayPasses.csv"

                return newFileName
            else:
                print(f"No matching data found for IdFile: {id_value}")
                return None
        else:
            print("The file name does not follow the expected pattern.")
            return None
    else:
        print("The file name does not have a CSV extension.")
        return None


def filterByPasses(dfRaw, clubName):
    finalDf = pd.DataFrame()
    # List of columns you want to add to the final DataFrame.
    columnsToAdd = [
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
    # Filter by club's parameter
    passes = dfNoNan.loc[
        (dfNoNan["type_id"] == "30") & (dfNoNan["team_name"] == clubName)
    ]
    # Calculate difference between target columns and df
    difference = set(columnsToAdd) - set(passes.columns)

    if difference:
        # There is difference
        finalDf = passes.reindex(columns=columnsToAdd)
    else:
        # All columns are present
        finalDf = passes.loc[:, columnsToAdd]
    return finalDf


# Main function to execute the program
def main():
    experimentName, clubName = getParameters()
    dataFolder, targetFolder, metadadaFile = generateDynamicPaths(experimentName)
    metadada = getMetaDataFile(metadadaFile, clubName)
    readFolderFiles(dataFolder, targetFolder, clubName, metadada)


if __name__ == "__main__":
    main()
