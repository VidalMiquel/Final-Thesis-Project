import sys
import os
import json
import pandas as pd

# Function to get the experiment name from command-line arguments
def getExperimentName():
    if len(sys.argv) == 3:
        return sys.argv[1], sys.argv[2]
    else:
        print("ExperimentName has not been provided as an argument.")
        sys.exit(1)


# Function to generate dynamic paths for data and target folders
def generateDynamicPaths(experimentName):
    currentDir = os.path.abspath(
        os.path.dirname(__file__)
    )  # Get the current directory of the script

    dataFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "FirstStage", "TargetFiles"
    )

    targetFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "SecondStage", "MiddleFiles"
    )

    if not os.path.exists(targetFolder):
        print(
            f"The folder {targetFolder} does not exist for experiment {experimentName}."
        )
        sys.exit(1)

    return dataFolder, targetFolder


import os

def getFileNamesInFolder(folderPath):
    try:
        if os.path.isdir(folderPath):
            files = os.listdir(folderPath)
            return files
        else:
            raise FileNotFoundError(f"The path '{folderPath}' is not a valid directory.")
    except OSError as e:
        raise OSError(f"Error accessing the directory: {e}")


# Function to iterate through files, read them, and perform operations
def iterateAndReadFiles(currentPath, targetPath, nameFiles, clubName):
    try:
        for fileName in nameFiles:
            filePath = os.path.join(currentPath, fileName)
            try:
                with open(filePath, "r", encoding="utf-8") as file:
                    content = json.load(file)
                    dataframe = pd.DataFrame(content)
                    divisionFiles, score = getGoals(dataframe)
                    splitList = getDivisionIndices(divisionFiles, len(dataframe))
                    generateMatchResults(score,clubName)
                    generateDivisionFiles(splitList, dataframe, fileName, targetPath)
            except OSError as e:
                print(f"Error reading the file '{fileName}': {e}")
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in '{fileName}': {e}")
    except OSError as e:
        print(f"Error accessing the path: {e}")
    
    
    
    
# Function to get division indices from the data
def getDivisionIndices(data, lenght):

    if not data.empty:
        
        divisionIndices = data.index.tolist()
        divisionIndices.insert(0, 0)
        divisionIndices.append(lenght)
        return divisionIndices
    else:
        #print("There are no divisions in 'data' as aux2 is empty.")
        return [0, lenght]  # Return [0, len(data)] as default values when no divisions are found

# Function to get division indices from the data
def getGoals(data):
   
    goalkeeperActions = data[data["type"].apply(lambda x: (x)["id"] == 23)]
    goals = goalkeeperActions[goalkeeperActions["goalkeeper"].apply(lambda x: (x)["type"]["id"] == 26 or (x)["type"]["id"] == 28)]  
    teamGoals1 = goals["possession_team"]
    
    ownGoals = data[data["type"].apply(lambda x: (x)["id"] == 25)]
    teamOwnGoals = ownGoals["team"]

    allGoals = pd.concat([teamGoals1, teamOwnGoals], axis=0)
    alternativeGoal = pd.concat([goals["possession_team"].apply(lambda x: x['name']),ownGoals["team"].apply(lambda x: x['name'])], axis = 0)
    sortedGoals = allGoals.sort_index()
    altertiveGoalSorted = alternativeGoal.sort_index()

    return sortedGoals, altertiveGoalSorted

def generateMatchResults(clubNames, ClubName):
    matchResults = []
    home_score = 0
    away_score = 0


    if clubNames.empty:
        matchResults.append("0_0")
    else:
         for club in clubNames:
            if club == ClubName:
                home_score += 1
            else:
                away_score += 1

            matchResults.append(f"{home_score}_{away_score}")
    
    return matchResults
# Function to generate division files based on indices
def generateDivisionFiles(indicesList, dataframe, fileName, targetPath,):
    try:
        if (len(indicesList) - 1) == 1:
            startIndex = indicesList[0]
            endIndex = indicesList[1]
            segment = dataframe.iloc[startIndex:endIndex]
            
            if not segment.empty:
                part = fileName.split("_")

            # Check if the filename has at least two underscores to ensure a valid split
            if len(part) >= 2:
                numberSegment = part[0]
                middleSegment = part[1]
                baseName, extension  = os.path.splitext(middleSegment)
                newFilename = f"{numberSegment}_{1}_{baseName}.json"
                filePath = os.path.join(targetPath, newFilename)
                segment.to_json(filePath, orient="records")
                    
        else:
            for i in range(len(indicesList) - 1):
                startIndex = indicesList[i]
                endIndex = indicesList[i + 1]

                segment = dataframe.iloc[startIndex:endIndex]
                
                if not segment.empty:
                    
                    # Split the filename into three segments
                    part = fileName.split("_")

                # Check if the filename has at least two underscores to ensure a valid split
                    if len(part) >= 2:
                        numberSegment = part[0]
                        middleSegment = part[1]
                        baseName, extension  = os.path.splitext(middleSegment)
                        newFilename = f"{numberSegment}_{i+1}_{baseName}.json"
                        filePath = os.path.join(targetPath, newFilename)

                        segment.to_json(filePath, orient="records")
                
    except Exception as e:
        print(f"Error generating division files: {e}")


# Main function to execute the program
def main():
    experimentName,clubName = getExperimentName()
    dataFolder, targetFolder = generateDynamicPaths(experimentName)
    nameFootballDayFiles = getFileNamesInFolder(dataFolder)

    iterateAndReadFiles(dataFolder, targetFolder, nameFootballDayFiles, clubName)


if __name__ == "__main__":
    main()
