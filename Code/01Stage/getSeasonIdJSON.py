import json
import os
import sys
import urllib.request


# Retrieves the experiment name from the command line arguments.
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


# Reads and parses a JSON file containing season data.
def getChosenSeasonDataJson(fileName):
    with open(fileName, "r") as file:
        data = json.load(file)
    return data


# Extracts the competitionId and seasonId from the JSON data.
def getParameters(data):
    results = data["results"]
    return results["competitionId"], results["seasonId"]


# Constructs the URL for downloading the match data JSON file.
def buildUrl(competitionId, seasonId):
    return f"https://github.com/VidalMiquel/Statsbomb/raw/master/data/matches/{competitionId}/{seasonId}.json"


# Downloads a file from the given URL and saves it to the specified location.
def downloadFile(url, fileName):
    try:
        urllib.request.urlretrieve(url, fileName)
        print(f"The file season_id.json has been downloaded successfully.")
    except Exception as e:
        print(f"Failed to download the file. Error: {e}")


def main():
    current_path = os.path.abspath(os.path.dirname(__file__))

    # Retrieve the experiment name from the command line arguments
    experiment_name = getExperimentName()
    if not experiment_name:
        sys.exit(1)

    # Define the input and output paths
    input_path = os.path.abspath(
        os.path.join(
            current_path, "..", "..", "Data", experiment_name, "01Stage", "MiddleFiles"
        )
    )
    output_path = os.path.abspath(
        os.path.join(
            current_path, "..", "..", "Data", experiment_name, "01Stage", "MiddleFiles"
        )
    )

    # Define the name and path of the chosen season data file
    chosen_season_file_name = "chosenSeasonData.json"
    chosen_season_file_path = os.path.join(input_path, chosen_season_file_name)

    # Load the chosen season data from the JSON file
    data_frame = getChosenSeasonDataJson(chosen_season_file_path)

    # Extract competitionId and seasonId from the data
    competition_id, season_id = getParameters(data_frame)

    # Build the URL for the match data JSON file
    url = buildUrl(competition_id, season_id)

    # Define the name and path for the downloaded file
    download_file_name = "seasonId.json"
    download_file_path = os.path.join(output_path, download_file_name)

    # Download the match data JSON file
    downloadFile(url, download_file_path)


if __name__ == "__main__":
    main()
