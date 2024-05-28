import json
import os
import sys
import urllib.request
from datetime import datetime


def toDayOfYear(date):
    # Convert the date string to a datetime object
    dateObject = datetime.strptime(date, "%Y-%m-%d")

    # Get the day of the year
    dayOfYear = dateObject.timetuple().tm_yday

    return dayOfYear


# Check if the proper arguments were provided
def getExperimentName():
    if len(sys.argv) != 2:
        print(
            "Please provide values for CompetitionName, CompetitionYear, CompetitionGender, and Club."
        )
        return None

    # Get the argument values
    experimentName = sys.argv[1]

    return experimentName


def main():
    experimentName = getExperimentName()

    # Get the directory path where the script is executed
    currentPath = os.path.abspath(os.path.dirname(__file__))

    # Path to 'id_matches.json' file from TFG/Code/01Stage/
    idMatchesPath = os.path.join(
        currentPath,
        "..",
        "..",
        "Data",
        experimentName,
        "01Stage",
        "MiddleFiles",
        "idMatches.json",
    )

    # Path where the downloaded files will be saved
    outputPath = os.path.join(
        currentPath, "..", "..", "Data", experimentName, "01Stage", "TargetFiles"
    )

    # Check if the 'id_matches.json' file exists
    if os.path.exists(idMatchesPath):
        # Open 'id_matches.json' file and load JSON data
        with open(idMatchesPath, "r") as idMatchesFile:
            idMatchesData = json.load(idMatchesFile)

        # Iterate through the keys (matchday numbers) and values (lists of matches) in 'id_matches.json'
        for matchday, matches in idMatchesData.items():
            day = toDayOfYear(matchday)
            matchId = matches[0]
            # Build URL with the current match_id
            url = f"https://raw.githubusercontent.com/VidalMiquel/Statsbomb/master/data/events/{matchId}.json"

            # File name to be saved, using the match_id
            fileName = f"{day}_footballDay.json"

            # Full path where the file will be saved
            filePath = os.path.join(outputPath, fileName)

            # Download the file from URL and save it to the specified path
            try:
                urllib.request.urlretrieve(url, filePath)
                # print(f"File {fileName} downloaded successfully.")
            except Exception as e:
                print(f"Failed to download file {fileName}. Error: {e}")
    else:
        print("The 'id_matches.json' file was not found at the specified location.")


if __name__ == "__main__":
    main()
