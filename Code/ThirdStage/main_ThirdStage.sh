#!/bin/bash

# Retrieve the experiment name from the first argument
experimentName="$1"

# Retrieve the club for the experiment from the second argument
club="$2"

# Get the current directory path
currentDirectory=$(dirname "$0")

# Change to the directory containing start_FirstStage.py
cd "$currentDirectory"

echo Executing ThirdStage...
echo ""
# Execute start_SecondStage.py
echo "Creating necessary directories with startThirdStage.py..."
python startThirdStage.py "$experimentName"
echo ""

# Execute start_SecondStage.py
echo "Flattening JSON files with flattenJSONfiles.py..."
python flattenJSONfiles.py "$experimentName"

echo ""  # Blank line
echo "Process completed."
echo ""  # Blank line
