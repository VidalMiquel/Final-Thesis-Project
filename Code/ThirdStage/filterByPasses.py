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
    #print(currentDir)
    dataFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "ThirdStage", "Middle_files"
    )
    #print(dataFolder)
    targetFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "ThirdStage", "Target_files"
    )
    #print(targetFolder)

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
        #print(newFileName)
        filePath = os.path.join(targetFolder, newFileName)
        try:
            data.to_csv(filePath, index = False, encoding = 'utf-8-sig')
            #print(f"File stored at: {filePath}")
        except Exception as e:
            print(f"Error while saving the file: {e}")
        #print(f"File '{newFileName}' generated successfully.")
    else:
        #print(data)
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
        df = pd.read_csv(filePath,dtype=str)
        filteredData = filterbyPasses(df, clubName)
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

def filterbyPasses(dfRaw, clubName):
    #Remove NaN values
    #dfNoNAn = dfRaw.dropna(axis = 1, how = 'all').dropna(axis = 0, how = 'all')
    #Get relation between id-name-position
    passes = dfRaw.loc[(dfRaw["type_id"] == "30") & (dfRaw["team_name"] == clubName)]
    return passes
    
    

# Main function to execute the program
def main():
    experimentName, clubName = getParameters()
    dataFolder, targetFolder = generateDynamicPaths(experimentName)
    readFolderFiles(dataFolder, targetFolder, clubName)



if __name__ == "__main__":
    main()
