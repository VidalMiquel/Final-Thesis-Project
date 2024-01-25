import os
import json
import urllib.request
import sys


def getExperimentName():
    # Check if the proper arguments were provided
    if len(sys.argv) != 2:
        print(
            "Please provide values for CompetitionName, CompetitionYear, CompetitionGender, and Club."
        )
        return None

    # Get the argument values
    experimentName = sys.argv[1]

    return experimentName


experimentName = getExperimentName()

# Get the directory path where the script is executed
currentPath = os.path.abspath(os.path.dirname(__file__))

# Path to 'id_matches.json' file from TFG/Code/FirstStage/
idMatchesPath = os.path.join(
    currentPath,
    "..",
    "..",
    "Data",
    experimentName,
    "FirstStage",
    "Middle_files",
    "id_matches.json",
)

# Path where the downloaded files will be saved
outputPath = os.path.join(
    currentPath, "..", "..", "Data", experimentName, "FirstStage", "Target_files"
)

# Check if the 'id_matches.json' file exists
if os.path.exists(idMatchesPath):
    # Open 'id_matches.json' file and load JSON data
    with open(idMatchesPath, "r") as idMatchesFile:
        idMatchesData = json.load(idMatchesFile)

    # Iterate through the keys (matchday numbers) and values (lists of matches) in 'id_matches.json'
    for matchday, matches in idMatchesData.items():
        for match_id in matches:
            # Build URL with the current match_id
            url = f"https://raw.githubusercontent.com/VidalMiquel/Statsbomb/master/data/events/{match_id}.json"

            # File name to be saved, using the match_id
            fileName = f"footballDay_{matchday}.json"

            # Full path where the file will be saved
            filePath = os.path.join(outputPath, fileName)

            # Download the file from URL and save it to the specified path
            try:
                urllib.request.urlretrieve(url, filePath)
                print(f"File {fileName} downloaded successfully.")
            except Exception as e:
                print(f"Failed to download file {fileName}. Error: {e}")
else:
    print(
        "The 'id_matches.json' file was not found at the specified location."
    )
