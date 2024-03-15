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
    except FileExistsError:
        pass    

    
def createFolderStructure(stage_name, experiment_name):
       # Get the absolute path of the current directory
    currentPath = os.path.abspath(os.path.dirname(__file__))

    # Build the absolute path of TFG/Data
    dataPath = os.path.abspath(os.path.join(currentPath, "..", "Data"))

    # Complete path for the "experimentName" folder within "Data"
    experimentNamePath = os.path.join(dataPath, experiment_name)

    # Complete path for the "FirstStage" folder within "Data"
    firstStagePath = os.path.join(experimentNamePath, stage_name)

    # Complete path for the "Middle_files" folder within "FirstStage"
    middleFilesPath = os.path.join(firstStagePath, "TargetFiles")

    # Complete path for the "Target_files" folder within "FirstStage"
    targetFilesPath = os.path.join(firstStagePath, "MiddleFiles")

    # Create the "Data" folder if it doesn't exist
    createDirectoryAbsolutePath(dataPath)

    # Create the "FirstStage" folder within "Data" if it doesn't exist
    createDirectoryAbsolutePath(firstStagePath)
        
    # Create the "Target_files" folder within "FirstStage" if it doesn't exist
    createDirectoryAbsolutePath(targetFilesPath)

    # Create the "Middle_files" folder within "FirstStage" if it doesn't exist
    createDirectoryAbsolutePath(middleFilesPath)



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py experiment_name stage_name")
        sys.exit(1)

    experiment_name = sys.argv[1]
    stage_name = sys.argv[2]
    
    if not stage_name:
        print("No stage name provided.")
        sys.exit(1)

    createFolderStructure(stage_name, experiment_name)
