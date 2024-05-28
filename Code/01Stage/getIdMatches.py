import json
import os
import sys


def getExperimentName():
    # Check if the appropriate arguments are provided
    if len(sys.argv) != 2:
        print(
            "Please provide values for CompetitionName, CompetitionYear, CompetitionGender, and Club."
        )
        return None

    # Get the values of the arguments
    experimentName = sys.argv[1]
    return experimentName


def filterMatchesByTeam(fileSeasonIdPath, teamName):
    experimentName = getExperimentName()
    # Get the path of the directory where the script is being executed
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
    # Path to the season data file
    seasonIdPath = os.path.join(outputPath, fileSeasonIdPath)

    try:
        # Open the JSON file containing the season data
        with open(seasonIdPath, "r", encoding="utf-8") as file:
            data = json.load(file)  # Load JSON data
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Dictionary to store matches filtered by the user-provided team
    selectedMatches = {}

    # Iterate through the data to filter matches by the user-provided team
    for match in data:
        homeTeam = match["home_team"]["home_team_name"]
        awayTeam = match["away_team"]["away_team_name"]

        # Check if the team name matches either the home or away team of the match
        if teamName.lower() == homeTeam.lower() or teamName.lower() == awayTeam.lower():
            # Get the match week number
            matchWeek = match["match_date"]
            matchId = match["match_id"]  # Get the match ID

            if matchWeek not in selectedMatches:
                # Initialize the list of matches if it's the first time encountering that match week
                selectedMatches[matchWeek] = []

            # Add the match ID to the list of selected matches for that match week
            selectedMatches[matchWeek].append(matchId)

    if not selectedMatches:
        raise Exception(f"We don't have data for the selected team: {teamName}")

    # Path to save the selected matches file
    outputPath = os.path.join(outputPath, "idMatches.json")

    # Write the selected matches to a JSON file
    with open(outputPath, "w") as outputFile:
        # Save the data to the JSON file with formatting
        json.dump(selectedMatches, outputFile, indent=4)


# Function to read chosen season data from a JSON file
def getChosenSeasonDataJson(filename):
    with open(filename, "r") as file:  # Open the file in read mode
        data = json.load(file)  # Load JSON data from the file
    return data


def getParameters(data):
    results = data["metadata"]  # Get the list of results
    return results[0]["club"]  # Return the club


def getClubValue():
    try:
        # Get the current directory path
        currentPath = os.path.abspath(os.path.dirname(__file__))

        experimentName = getExperimentName()
        # Define input and output paths
        filePath = os.path.abspath(
            os.path.join(
                currentPath,
                "..",
                "..",
                "Data",
                experimentName,
                "01Stage",
                "MiddleFiles",
                "chosenSeasonData.json",
            )
        )

        # Check if the file exists
        if not os.path.exists(filePath):
            raise FileNotFoundError(f"The file {filePath} was not found.")

        # Read the JSON file
        with open(filePath, "r") as file:
            data = json.load(file)

            # Get the value of 'club' from the JSON file
            club = data["metadata"]["club"]
            return club

    except FileNotFoundError as e:
        return str(e)
    except KeyError:
        return "The 'club' value is not present in the JSON file."


def main():
    try:
        # Call the function to get the 'club' value
        clubValue = getClubValue()
        # Filter matches of the entered team and save IDs to a JSON file
        filterMatchesByTeam("seasonId.json", clubValue)
        print("The match IDs have been successfully obtained.")
    except Exception as e:
        print(f"We don't have data for the selected team: {clubValue}")
        sys.exit(1)


if __name__ == "__main__":
    main()
