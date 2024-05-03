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

    # Name of the folder "experimentName"
    experimentNameFolder = getExperimentName()

    # Complete path for the "experimentName" folder within "Data"
    experimentNamePath = os.path.join(dataPath, experimentNameFolder)

    # Name of the folder "ThirdStage"
    thirdStageFolderName = "ThirdStage"

    # Complete path for the "ThirdStage" folder within "Data"
    thirdStagePath = os.path.join(experimentNamePath, thirdStageFolderName)

    # Complete path for the "MiddleFiles" folder within "ThirdStage"
    middleFilesPath = os.path.join(thirdStagePath, "MiddleFiles")

    # Complete path for the "TargetFiles" folder within "ThirdStage"
    targetFilesPath = os.path.join(thirdStagePath, "TargetFiles")

    # Create the "ThirdStage" folder within "Data" if it doesn't exist
    createDirectoryAbsolutePath(thirdStagePath)

    # Create the "MiddleFiles" folder within "ThirdStage" if it doesn't exist
    createDirectoryAbsolutePath(middleFilesPath)

    # Create the "TargetFiles" folder within "ThirdStage" if it doesn't exist
    createDirectoryAbsolutePath(targetFilesPath)


# Call the function to create the folder structure
createFolderStructure()
