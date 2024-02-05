#!/bin/bash

# Retrieve the experiment name from the first argument
experimentName="$1"

# Retrieve the club for the experiment from the second argument
club="$2"

# Get the current directory path
currentDirectory=$(dirname "$0")

# Change to the directory containing startThirdStage.py
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
echo " "


# Execute start_SecondStage.py
echo "Filtering CSV files with filterByPasses.py..."
python filterByPasses.py "$experimentName" "$club"


echo ""  # Blank line
echo "Third Stage completed."
echo ""  # Blank line
echo "------------------------------------------"
echo ""  # Blank line
