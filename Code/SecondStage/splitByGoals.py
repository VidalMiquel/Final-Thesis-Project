from decimal import DivisionByZero
import sys
import os
import json
import pandas as pd


# Function to get the experiment name from command-line arguments
def getExperimentName():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        print("ExperimentName has not been provided as an argument.")
        sys.exit(1)


# Function to generate dynamic paths for data and target folders
def generateDynamicPaths(experimentName):
    currentDir = os.path.abspath(
        os.path.dirname(__file__)
    )  # Get the current directory of the script

    dataFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "FirstStage", "Target_files"
    )

    targetFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "SecondStage", "Middle_files"
    )

    if not os.path.exists(targetFolder):
        print(
            f"The folder {targetFolder} does not exist for experiment {
                experimentName}."
        )
        sys.exit(1)

    return dataFolder, targetFolder


# Function to count files in a folder
def countFilesInFolder(folderPath):
    try:
        if os.path.isdir(folderPath):
            files = os.listdir(folderPath)
            numFiles = len(files)
            return numFiles
        else:
            print(f"The path {folderPath} is not a valid directory.")
            return None
    except OSError as e:
        print(f"Error accessing the directory: {e}")
        return None


# Function to iterate through files in a folder and check their existence
def iterateAndCheckFiles(currentPath, numFiles):
    try:
        for i in range(1, numFiles + 1):
            fileName = f"footballDay_{i}.json"
            filePath = os.path.join(currentPath, fileName)
            if not (os.path.exists(filePath) and os.path.isfile(filePath)):
                print(f"The file '{fileName}' was not found.")     
    except OSError as e:
        print(f"Error accessing the path: {e}")


# Function to iterate through files, read them, and perform operations
def iterateAndReadFiles(currentPath, targetPath, numFiles):
    try:
        for i in range(1, numFiles + 1):
            fileName = f"footballDay_{i}.json"
            filePath = os.path.join(currentPath, fileName)
            try:
                with open(filePath, "r", encoding="utf-8") as file:
                    content = json.load(file)
                    dFrame = pd.DataFrame(content)
                    splitList = getDivisionIndices(dFrame)
                    generateDivisionFiles(splitList, dFrame, i, targetPath)
            except OSError as e:
                print(f"Error reading the file '{fileName}': {e}")
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in '{fileName}': {e}")
    except OSError as e:
        print(f"Error accessing the path: {e}")


# Function to get division indices from the data
def getDivisionIndices(data):
    auxiliar = data[data["type"].apply(lambda x: (x)["id"] == 23)]
    aux2 = auxiliar[auxiliar["goalkeeper"].apply(lambda x: (x)["type"]["id"] == 26)]

    if not aux2.empty:
        divisionIndices = aux2.index.tolist()
        divisionIndices.insert(0, 0)
        divisionIndices.append(len(data))
        return divisionIndices
    else:
        print("There are no divisions in 'data' as aux2 is empty.")
        return [0, len(data)]  # Return [0, len(data)] as default values when no divisions are found


# Function to generate division files based on indices
def generateDivisionFiles(indicesList, dataframe, jornadaValue, targetPath):
    try:
        for i in range(len(indicesList) - 1):
            startIndex = indicesList[i]
            endIndex = indicesList[i + 1]

            segment = dataframe.iloc[startIndex:endIndex]

            if not segment.empty:
                fileName = f"footballDay_{jornadaValue}_{i+1}.json"
                filePath = os.path.join(targetPath, fileName)

                segment.to_json(filePath, orient="records")
            else:
                print(
                    f"The segment {
                        i+1} for the jornada {jornadaValue} is empty, no file will be generated."
                )
    except Exception as e:
        print(f"Error generating division files: {e}")


# Main function to execute the program
def main():
    experimentName = getExperimentName()
    dataFolder, targetFolder = generateDynamicPaths(experimentName)
    numFootballDayFiles = countFilesInFolder(dataFolder)

    iterateAndReadFiles(dataFolder, targetFolder, numFootballDayFiles)


if __name__ == "__main__":
    main()
