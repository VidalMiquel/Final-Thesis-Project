import sys
import os
import json
import pandas as pd

metadataContent = []  # Initialize an empty list for metadata content

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
        currentDir, "..", "..", "Data", experimentName, "01Stage", "TargetFiles"
    )

    targetFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "02Stage", "MiddleFiles"
    )

    if not os.path.exists(targetFolder):
        print(
            f"The folder {targetFolder} does not exist for experiment {experimentName}."
        )
        sys.exit(1)

    return dataFolder, targetFolder


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
def iterateAndManagmentFiles(currentPath, targetPath, nameFiles, clubName, experimentName):
    try:
        for fileName in nameFiles:
            filePath = os.path.join(currentPath, fileName)
            try:
                with open(filePath, "r", encoding="utf-8") as file:
                    content = json.load(file)
                    dataFrame = pd.DataFrame(content)
                    divisionFiles = getGoals(dataFrame)
                    teamGoals = getScore(dataFrame)
                    splitList = getDivisionIndices(divisionFiles, len(dataFrame))
                    scoreDifference, resultsForSplit = generateMatchResults(teamGoals,clubName)
                    newFileName = generateDivisionFiles(splitList, dataFrame, fileName, targetPath)
                    metadataFile = generateMetadataFile(teamGoals, resultsForSplit, newFileName, scoreDifference)
            except OSError as e:
                print(f"Error reading the file '{fileName}': {e}")
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in '{fileName}': {e}")
        #print(metadataFile)
        saveFilteredFile(metadataFile, experimentName, clubName)
    except OSError as e:
        print(f"Error accessing the path: {e}")
    
# Function to save filtered data to a file
def saveFilteredFile(data, experimentName, clubName):
    
    currentDir = os.path.abspath(
        os.path.dirname(__file__)
    )
    
    targetFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "02Stage"
    )
    # Check if the segment is not empty before saving

    df = pd.DataFrame(data)
    df.columns = ["IdFiles", "ScoringTeam", "Score", "Difference", "NoInformation"]
    
    if data:
        # File name in the format Football_day_n_m
        filePath = os.path.join(targetFolder, f"metadata{clubName}.csv")
        try:
            df.to_csv(filePath, index=False, encoding="utf-8-sig")
        except Exception as e:
            print(f"Error while saving the file: {e}")
    else:
        # print(data)
        print(f"The file is empty, no file will be generated: ")


def separateFileName(fileName):
    correctPart = []
    for name in fileName:
        parts = name.split("_")
        firstPart = "_".join(parts[:2])
        correctPart.append(firstPart)
    return correctPart
    
        
def generateMetadataFile(teamGoals, scorerSplit, fileName, scoreDifference):
    idFiles = separateFileName(fileName)

    if  teamGoals.empty:
        metadataContent.append((idFiles[0], None, None, "NF"))
    else:
            # Create tuples and append them to metadataContent
        for team, scorer, idFile, difference in zip(teamGoals, scorerSplit, idFiles, scoreDifference):
            metadataContent.append((idFile, team, scorer, int(difference), None)) 
        metadataContent.append((idFiles[-1], None, "NF", "NF", "NF"))
    return metadataContent

    
        

def getGoals(data):
       
    goalkeeperActions = data[data["type"].apply(lambda x: (x)["id"] == 23)]
    goals = goalkeeperActions[goalkeeperActions["goalkeeper"].apply(lambda x: (x)["type"]["id"] == 26 or (x)["type"]["id"] == 28)]  
    teamGoals1 = goals["possession_team"]
    
    ownGoals = data[data["type"].apply(lambda x: (x)["id"] == 25)]
    teamOwnGoals = ownGoals["team"]

    allGoals = pd.concat([teamGoals1, teamOwnGoals], axis=0)

    sortedGoals = allGoals.sort_index()


    return sortedGoals

def getScore(data):
    
    goalkeeperActions = data[data["type"].apply(lambda x: (x)["id"] == 23)]
    goals = goalkeeperActions[goalkeeperActions["goalkeeper"].apply(lambda x: (x)["type"]["id"] == 26 or (x)["type"]["id"] == 28)]  
    
    ownGoals = data[data["type"].apply(lambda x: (x)["id"] == 25)]

    nameTeamGoal = pd.concat([goals["possession_team"].apply(lambda x: x['name']),ownGoals["team"].apply(lambda x: x['name'])], axis = 0)

    return nameTeamGoal.sort_index()


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
    
    ownGoals = data[data["type"].apply(lambda x: (x)["id"] == 25)]
    

    allGoals = pd.concat([goals, ownGoals], axis=0)

    sortedGoals = allGoals.sort_index()
    
    return sortedGoals

def generateMatchResults(clubNames, ClubName):
    matchResults = []
    resultDifferences = []
    home_score = 0
    away_score = 0


    if clubNames.empty:
        matchResults.append(f"{home_score}_{away_score}")
    else:
         for club in clubNames:
            if club == ClubName:
                home_score += 1
            else:
                away_score += 1

            matchResults.append(f"{home_score}_{away_score}")
            resultDifferences.append(home_score - away_score)
            
    return resultDifferences, matchResults

#def generateMetadataFiles(teams, scores):
    

def generateDivisionFiles(indicesList, dataframe, fileName, targetPath):
    fileNameList = []
    try:
        for i in range(len(indicesList) - 1):
            startIndex = indicesList[i]
            endIndex = indicesList[i + 1]
            segment = dataframe.iloc[startIndex:endIndex]

            if not segment.empty:
                part = fileName.split("_")
                numberSegment = part[0]
                middleSegment = part[1]
                baseName, extension = os.path.splitext(middleSegment)
                
                if (len(indicesList) - 1) == 1:
                    segmentIndex = 1
                else:
                    segmentIndex = i + 1

                newFileName = f"{numberSegment}_{segmentIndex}_{baseName}.json"
                fileNameList.append(newFileName)
                #print(fileNameList)
                filePath = os.path.join(targetPath, newFileName)
                segment.to_json(filePath, orient="records")
        return fileNameList
    except Exception as e:
        print(f"Error generating division files: {e}")
        


# Main function to execute the program
def main():
    experimentName,clubName = getExperimentName()
    dataFolder, targetFolder = generateDynamicPaths(experimentName)
    nameFootballDayFiles = getFileNamesInFolder(dataFolder)

    iterateAndManagmentFiles(dataFolder, targetFolder, nameFootballDayFiles, clubName, experimentName)


if __name__ == "__main__":
    main()
