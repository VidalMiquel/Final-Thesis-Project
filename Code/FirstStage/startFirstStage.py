import os
import sys

def getExperimentName():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        return None

def createDirectoryAbsolutePath(path):
    try:
        os.makedirs(path)
        #print(f"Created folder at {path}")
    except FileExistsError:
        print(f"The folder at {path} already exists.")

def createFolderStructure():
    # Get the absolute path of the current directory
    currentPath = os.path.abspath(os.path.dirname(__file__))

    # Build the absolute path of TFG/Data
    dataPath = os.path.abspath(os.path.join(currentPath, "..", "..", "Data"))

    # Name of the "experimentName" folder
    experimentNameFolder = getExperimentName()

    # Complete path for the "experimentName" folder within "Data"
    experimentNamePath = os.path.join(dataPath, experimentNameFolder)

    # Name of the "FirstStage" folder
    firstStageFolderName = "FirstStage"

    # Complete path for the "FirstStage" folder within "Data"
    firstStagePath = os.path.join(experimentNamePath, firstStageFolderName)

    # Complete path for the "Middle_files" folder within "FirstStage"
    middleFilesPath = os.path.join(firstStagePath, "MiddleFiles")

    # Complete path for the "Target_files" folder within "FirstStage"
    targetFilesPath = os.path.join(firstStagePath, "TargetFiles")

    # Create the "Data" folder if it doesn't exist
    createDirectoryAbsolutePath(dataPath)

    # Create the "FirstStage" folder within "Data" if it doesn't exist
    createDirectoryAbsolutePath(firstStagePath)

    # Create the "Middle_files" folder within "FirstStage" if it doesn't exist
    createDirectoryAbsolutePath(middleFilesPath)

    # Create the "Target_files" folder within "FirstStage" if it doesn't exist
    createDirectoryAbsolutePath(targetFilesPath)

# Call the function to create the folder structure
createFolderStructure()
