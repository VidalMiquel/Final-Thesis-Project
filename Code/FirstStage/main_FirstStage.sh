#!/bin/bash

# Get the experiment name from the first argument
experimentName="$1"

# Get the club value for the experiment from the second argument
club="$2"

# Get the current directory path
currentDirectory=$(dirname "$0")

# Change to the directory containing start_FirstStage.py
cd "$currentDirectory"

# Prompt the user for CompetitionName, CompetitionYear, CompetitionGender, and Club values
echo ""
echo "Enter the competition name (competitionName):"
read competitionName

echo ""
echo "Enter the competition year (competitionYear):"
read competitionYear

echo ""
echo "Enter the competition gender (competitionGender):"
read competitionGender

echo ""
echo "Executing FirstStage..."


# Execute start_FirstStage.py
echo "Creating necessary directories with start_FirstStage.py..."
python start_FirstStage.py "$experimentName"

# Add blank lines to separate sections
echo ""
echo "Executing get_season_information.py with the provided parameters..."
python get_season_information.py "$competitionName" "$competitionYear" "$competitionGender" "$club" "$experimentName"

# Execute get_season_id_json.py
echo "" # Blank line
echo "Executing get_season_id_json.py..."
python get_season_id_json.py "$experimentName"

# Execute get_id_matches.py
echo "" # Blank line
echo "Executing get_id_matches.py..."
python get_id_matches.py "$experimentName"

# Execute get_target_files.py
echo "" # Blank line
echo "Executing get_target_files.py..."
python get_target_files.py "$experimentName"

# Add a blank line at the end of the process
echo "" # Last blank line
echo "Data collection process completed."

