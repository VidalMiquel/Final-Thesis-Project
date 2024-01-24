import json
import urllib.request
import os
import sys
import pandas as pd

def getSeasonInformation():
    # Verify if the correct arguments are provided
    if len(sys.argv) != 6:
        print("Please provide values for CompetitionName, CompetitionYear, CompetitionGender, and Club.")
        sys.exit(1)

    # Get the values of the arguments
    return tuple(sys.argv[1:])

# Function to read a JSON file from a URL
def readJsonFromUrl(url):
    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)
            return data  # Return the content of the JSON file
    except Exception as e:
        print(f"Error reading file from URL: {e}")
        sys.exit(1)

def searchMatch(data, competitionName, competitionGender, seasonName):
    try:
        df = pd.DataFrame(data)
        filtered_df = df[
            (df["competition_name"] == competitionName)
            & (df["competition_gender"] == competitionGender)
            & (df["season_name"] == seasonName)
        ]

        if filtered_df.empty:
            print("\nNo matches found for the provided values:\n -Competition gender: ", competitionGender, "\n -Competition name: ", competitionName, "\n -Season name: ", seasonName)
            sys.exit(1)

        result_dict = {
            "competitionId": int(filtered_df["competition_id"].values[0]),
            "seasonId": int(filtered_df["season_id"].values[0])
        }

        return result_dict
    except pd.errors.EmptyDataError as e:
        print(f"No data found for the provided values: {e}")
        sys.exit(1)
    except IndexError as e:
        print(f"Index error: {e}")
        sys.exit(1)

def getOutputPath():
    currentPath = os.path.abspath(os.path.dirname(__file__))
    outputPath = os.path.abspath(
        os.path.join(
            currentPath,
            "..",
            "..",
            "Data",
            experimentName,
            "FirstStage",
            "Middle_files",
        )
    )
    return outputPath

def saveJsonData(searchResults, competitionName, competitionGender, seasonName, club, experimentName):
    filename = "chosen_season_data.json"
    outputPath = getOutputPath()
    completeFilePath = os.path.join(outputPath, filename)

    try:
        if not os.path.exists(outputPath):
            os.makedirs(outputPath)

        # Create a dictionary to store metadata
        metadata = {
            "metadata": {
                "competition_name": competitionName,
                "competition_gender": competitionGender,
                "season_name": seasonName,
                "club": club,
                "experimentName": experimentName,
            },
            "results": searchResults,
        }

        with open(completeFilePath, "w", encoding="utf-8") as file:
            json.dump(metadata, file, indent=4)
        print(
            f'Data has been saved in the file "{filename}" in the output folder successfully.'
        )
    except Exception as e:
        print(f"Error saving JSON file: {e}")

# URL of the competitions.json file
urlCompetitionsJson = (
    "https://github.com/VidalMiquel/Statsbomb/raw/master/data/competitions.json"
)

# Read the contents of the competitions.json file from the URL
jsonData = readJsonFromUrl(urlCompetitionsJson)

if jsonData is not None:
    try:
        values = getSeasonInformation()

        if values:
            (
                competitionName,
                competitionYear,
                competitionGender,
                club,
                experimentName,
            ) = values

        # Further operations using these values can be performed here in your script
        # For instance, passing these values to other functions or performing specific logic
        # based on these variables can be done from this point onwards.
        searchResults = searchMatch(
            jsonData, competitionName, competitionGender, competitionYear
        )

        if searchResults:
            saveJsonData(
                searchResults,
                competitionName,
                competitionGender,
                competitionYear,
                club,
                experimentName,
            )
        else:
            print("No matches found for the provided values:", {values})

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
