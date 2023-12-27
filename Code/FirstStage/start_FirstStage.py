import os
import sys

def get_experiment_name():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        return None

def create_directory_absolute_path(path):
    try:
        os.makedirs(path)
        print(f"Created folder at {path}")
    except FileExistsError:
        print(f"The folder at {path} already exists.")

def create_folder_structure():
    # Get the absolute path of the current directory
    current_path = os.path.abspath(os.path.dirname(__file__))

    # Build the absolute path of TFG/Data
    data_path = os.path.abspath(os.path.join(current_path, "..", "..", "Data"))

    # Name of the "experimentName" folder
    experiment_name_folder = get_experiment_name()

    # Complete path for the "experimentName" folder within "Data"
    experiment_name_path = os.path.join(data_path, experiment_name_folder)

    # Name of the "FirstStage" folder
    first_stage_folder_name = "FirstStage"

    # Complete path for the "FirstStage" folder within "Data"
    first_stage_path = os.path.join(experiment_name_path, first_stage_folder_name)

    # Complete path for the "Middle_files" folder within "FirstStage"
    middle_files_path = os.path.join(first_stage_path, "Middle_files")

    # Complete path for the "Target_files" folder within "FirstStage"
    target_files_path = os.path.join(first_stage_path, "Target_files")

    # Create the "Data" folder if it doesn't exist
    create_directory_absolute_path(data_path)

    # Create the "FirstStage" folder within "Data" if it doesn't exist
    create_directory_absolute_path(first_stage_path)

    # Create the "Middle_files" folder within "FirstStage" if it doesn't exist
    create_directory_absolute_path(middle_files_path)

    # Create the "Target_files" folder within "FirstStage" if it doesn't exist
    create_directory_absolute_path(target_files_path)

# Call the function to create the folder structure
create_folder_structure()
