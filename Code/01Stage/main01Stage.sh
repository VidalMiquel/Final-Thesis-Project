#!/bin/bash

# Get the experiment name from the first argument
experimentName="$1"

# Get the club value for the experiment from the second argument
club="$2"

# Get the current directory path
currentDirectory=$(dirname "$0")

# Change to the directory containing start01Stage.py
cd "$currentDirectory"

# Prompt the user for CompetitionName, CompetitionYear and CompetitionGender values

read -p "Enter the competition's name: " competitionName
echo "" # Blank line

read -p "Enter the competition's year: " competitionYear
echo "" # Blank line

read -p "Enter the competition's gender: " competitionGender

echo "------------------------------------------"

echo "" # Blank line
echo Executing "01Stage"...
echo "" # Blank line

# Execute getSeasonInformation.py with error checking
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

# Execute getIdMmatches.py with error checking
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
echo "01Stage completed."
echo ""  # Blank line
echo "------------------------------------------"

