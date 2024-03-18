import os
import sys

def getExperimentName():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        return None

def createFolderAbsolutePath(path):
    try:
        os.makedirs(path)
        #print(f"Folder created at {path}")
    except FileExistsError:
        print(f"The folder at {path} already exists.")

def createFolderStructure():
    # Get the absolute path of the current directory
    currentPath = os.path.abspath(os.path.dirname(__file__))

    # Construct the absolute path of TFG/Data
    dataPath = os.path.abspath(os.path.join(currentPath, "..", "..", "Data"))

    # Name of the folder "experimentName"
    experimentNameFolderName = getExperimentName()

    # Complete path for the "experimentName" folder inside "Data"
    experimentNamePath = os.path.join(dataPath, experimentNameFolderName)

    # Name of the folder "FirstStage"
    firstStageFolderName = "SecondStage"

    # Complete path for the "FirstStage" folder inside "Data"
    secondStagePath = os.path.join(experimentNamePath, firstStageFolderName)

    # Complete path for the "MiddleFiles" folder inside "FirstStage"
    middleFilesPath = os.path.join(secondStagePath, "MiddleFiles")

    # Complete path for the "TargetFiles" folder inside "FirstStage"
    targetFilesPath = os.path.join(secondStagePath, "TargetFiles")

    # Create the "FirstStage" folder inside "Data" if it doesn't exist
    createFolderAbsolutePath(secondStagePath)

    # Create the "MiddleFiles" folder inside "FirstStage" if it doesn't exist
    createFolderAbsolutePath(middleFilesPath)

    # Create the "TargetFiles" folder inside "FirstStage" if it doesn't exist
    createFolderAbsolutePath(targetFilesPath)

# Call the function to create the folder structure
createFolderStructure()
