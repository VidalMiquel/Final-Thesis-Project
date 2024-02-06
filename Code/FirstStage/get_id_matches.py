import json
import os
import sys


def get_experiment_name():
    # Check if the appropriate arguments are provided
    if len(sys.argv) != 2:
        print(
            "Please provide values for CompetitionName, CompetitionYear, CompetitionGender, and Club."
        )
        return None

    # Get the values of the arguments
    experiment_name = sys.argv[1]
    return experiment_name


def filter_matches_by_team(file_season_id_path, team_name):
    experiment_name = get_experiment_name()
    # Get the path of the directory where the script is being executed
    current_path = os.path.abspath(os.path.dirname(__file__))
    output_path = os.path.abspath(
        os.path.join(
            current_path,
            "..",
            "..",
            "Data",
            experiment_name,
            "FirstStage",
            "Middle_files",
        )
    )
    # Path to the season data file
    season_id_path = os.path.join(output_path, file_season_id_path)

    try:
        # Open the JSON file containing the season data
        with open(season_id_path, "r", encoding="utf-8") as file:
            data = json.load(file)  # Load JSON data
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Dictionary to store matches filtered by the user-provided team
    selected_matches = {}

    # Iterate through the data to filter matches by the user-provided team
    for match in data:
        home_team = match["home_team"]["home_team_name"]
        away_team = match["away_team"]["away_team_name"]

        # Check if the team name matches either the home or away team of the match
        if (
            team_name.lower() == home_team.lower()
            or team_name.lower() == away_team.lower()
        ):
            # Get the match week number
            match_week = match["match_date"]
            match_id = match["match_id"]  # Get the match ID

            if match_week not in selected_matches:
                # Initialize the list of matches if it's the first time encountering that match week
                selected_matches[match_week] = []

            # Add the match ID to the list of selected matches for that match week
            selected_matches[match_week].append(match_id)

    if not selected_matches:
        raise Exception(f"We don't have data for the selected team: {team_name}")
    
    # Path to save the selected matches file
    output_path = os.path.join(output_path, "id_matches.json")

    # Write the selected matches to a JSON file
    with open(output_path, "w") as output_file:
        # Save the data to the JSON file with formatting
        json.dump(selected_matches, output_file, indent=4)


# Function to read chosen season data from a JSON file
def get_chosen_season_data_json(filename):
    with open(filename, "r") as file:  # Open the file in read mode
        data = json.load(file)  # Load JSON data from the file
    return data


def get_parameters(data):
    results = data["metadata"]  # Get the list of results
    return results[0]["club"]  # Return the club


def get_club_value():
    try:
        # Get the current directory path
        current_path = os.path.abspath(os.path.dirname(__file__))

        experiment_name = get_experiment_name()
        # Define input and output paths
        file_path = os.path.abspath(
            os.path.join(
                current_path,
                "..",
                "..",
                "Data",
                experiment_name,
                "FirstStage",
                "Middle_files",
                "chosen_season_data.json",
            )
        )

        # Check if the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} was not found.")

        # Read the JSON file
        with open(file_path, "r") as file:
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
        club_value = get_club_value()
        # Filter matches of the entered team and save IDs to a JSON file
        filter_matches_by_team("season_id.json", club_value)
        print("The match IDs have been successfully obtained.")
    except Exception as e:
        print(f"We don't have data for the selected team: {club_value}")
        sys.exit(1)


if __name__ == "__main__":
    main()
