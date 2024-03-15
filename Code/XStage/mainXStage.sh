#!/bin/bash

# Retrieve the experiment name from the first argument
experimentName="$1"

# Retrieve the club for the experiment from the second argument
club="$2"

# Get the current directory path
currentDirectory=$(dirname "$0")

# Change to the directory containing startFourthStage.py
cd "$currentDirectory"

echo Executing XStage...
echo "" # Blank line

# Execute start_SecondStage.py
echo "Generating graph from csv file exectuing generateGrpah.py"
python generateGraph.py "$experimentName"
echo "generateGraph.py executed successfully."

echo ""  # Blank line
echo "XSatge completed."
echo ""  # Blank line
echo "------------------------------------------"
