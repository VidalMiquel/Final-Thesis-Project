#!/bin/bash

# Retrieve the experiment name from the first argument
experimentName="$1"

# Retrieve the club for the experiment from the second argument
club="$2"

# Get the current directory path
currentDirectory=$(dirname "$0")

# Change to the directory containing startFourthStage.py
cd "$currentDirectory"

echo Executing "04Stage"...
echo "" # Blank line

# Execute generateGraph.py
echo "Generating graph from csv file exectuing generateGrpah.py"
python generateGraph.py "$experimentName"
echo "generateGraph.py executed successfully."

echo ""  # Blank line
echo "04Satge completed."
echo ""  # Blank line
echo "------------------------------------------"
