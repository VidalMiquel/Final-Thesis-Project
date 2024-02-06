#!/bin/bash

# Get the experiment name from the first argument
experimentName="$1"

# Get the club value for the experiment from the second argument
club="$2"

# Get the current directory path
currentDirectory=$(dirname "$0")

# Change to the directory containing startFirstStage.py
cd "$currentDirectory"

# Prompt the user for CompetitionName, CompetitionYear, CompetitionGender, and Club values
echo "Enter the competition name:"
read competitionName

echo "" # Blank line
echo "Enter the competition year:"
read competitionYear

echo "" # Blank line
echo "Enter the competition gender:"
read competitionGender
echo "------------------------------------------"

echo "" # Blank line
echo "Executing FirstStage..."
echo "" # Blank line

# Execute startFirstStage.py
echo "Creating necessary directories with startFirstStage.py..."
python startFirstStage.py "$experimentName"

# Execute getSeasonInformation.py with error checking
echo "" # Blank line
echo "Executing getSeasonInformation.py with the provided parameters..."
if python getSeasonInformation.py "$competitionName" "$competitionYear" "$competitionGender" "$club" "$experimentName"; then
    echo "getSeasonInformation.py executed successfully."
else
    exit 1
fi

# Execute getSeasonIdJSON.py with error checking
echo "" # Blank line
echo "Executing getSeasonIdJSON.py..."
if python getSeasonIdJSON.py "$experimentName"; then
    echo "getSeasonIdJSON.py executed successfully."
else
    exit 1
fi

# Execute get_id_matches.py with error checking
echo "" # Blank line
echo "Executing getIdMatches.py..."
if python getIdMatches.py "$experimentName"; then
    echo "getIdMatches.py executed successfully."
else
    exit 1
fi

# Execute getTargetFiles.py with error checking
echo "" # Blank line
echo "Executing getTargetFiles.py..."
if python getTargetFiles.py "$experimentName"; then
    echo "getTargetFiles.py executed successfully."
else
    exit 1
fi

echo ""  # Blank line
echo "FirstStage completed."
echo ""  # Blank line
echo "------------------------------------------"

