import json
import os
import sys
import urllib.request

import pandas as pd


# Verifies if the correct arguments are provided and returns them.
def getSeasonInformation():
    if len(sys.argv) != 6:
        print(
            "Please provide values for CompetitionName, CompetitionYear, CompetitionGender, and Club."
        )
        raise ValueError("Invalid number of arguments")

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
        raise  # Re-raise the exception


# Searches for a match in the JSON data based on the provided criteria.
def searchMatch(data, competitionName, competitionGender, seasonName):
    try:
        df = pd.DataFrame(data)
        filtered_df = df[
            (df["competition_name"] == competitionName)
            & (df["competition_gender"] == competitionGender)
            & (df["season_name"] == seasonName)
        ]

        if filtered_df.empty:
            print(
                "\nNo matches found for the provided values:\n\n -Competition name: "
                + competitionName
                + "\n\n -Competition gender: "
                + competitionGender
                + "\n\n -Season name: "
                + seasonName
                + "\n"
            )

            raise

        result_dict = {
            "competitionId": int(filtered_df["competition_id"].values[0]),
            "seasonId": int(filtered_df["season_id"].values[0]),
        }

        return result_dict
    except Exception as e:
        raise  # Re-raise the exception


# Constructs the output path for saving the JSON data.
def getOutputPath(experimentName):
    currentPath = os.path.abspath(os.path.dirname(__file__))
    outputPath = os.path.abspath(
        os.path.join(
            currentPath,
            "..",
            "..",
            "Data",
            experimentName,
            "01Stage",
            "MiddleFiles",
        )
    )
    return outputPath


# Saves the search results and metadata to a JSON file.
def saveJsonData(
    searchResults, competitionName, competitionGender, seasonName, club, experimentName
):
    filename = "chosenSeasonData.json"
    outputPath = getOutputPath(experimentName)
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
        raise  # Re-raise the exception


def main():
    # URL of the competitions.json file on GitHub
    urlCompetitionsJson = (
        "https://github.com/VidalMiquel/Statsbomb/raw/master/data/competitions.json"
    )

    try:
        # Read the JSON data from the URL
        jsonData = readJsonFromUrl(urlCompetitionsJson)

        # Check if JSON data was successfully retrieved
        if jsonData is not None:
            # Get the season information from command line arguments
            values = getSeasonInformation()

            if values:
                # Unpack the values into respective variables
                (
                    competitionName,
                    competitionYear,
                    competitionGender,
                    club,
                    experimentName,
                ) = values

                # Search for the match based on the provided competition details
                searchResults = searchMatch(
                    jsonData, competitionName, competitionGender, competitionYear
                )

                # If search results are found, save the JSON data
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
                    # Raise an error if no matches are found
                    raise ValueError("No matches found for the provided values.")
    except Exception as e:
        # Print the error message and exit the script if an exception occurs
        print(f"Error: {e}")
        sys.exit(1)


# Ensure the script runs only when executed directly
if __name__ == "__main__":
    main()
