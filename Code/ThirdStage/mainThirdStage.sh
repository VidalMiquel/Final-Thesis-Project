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
echo "" # Blank line
# Execute start_SecondStage.py
echo "Creating necessary directories with startThirdStage.py..."
python startThirdStage.py "$experimentName"
echo "startThirdStage.py executed successfully."
echo "" # Blank line


# Execute start_SecondStage.py
echo "Flattening JSON files and save them wih CSV format with flattenJSONfiles.py..."
python flattenJSONfiles.py "$experimentName"
echo "flattenJSONfiles.py executed successfully."
echo " " # Blank line


# Execute start_SecondStage.py
echo "Filtering CSV files with filterByPasses.py..."
python filterByPasses.py "$experimentName" "$club"
echo "filterByPasses.py executed successfully."
echo " " # Blank line

# Execute start_SecondStage.py
echo "Generating final metadata file with generateMetaDataFile.py..."
python generateMetaDataFile.py "$experimentName" "$club"
echo "generateMetaDataFile.py executed successfully."

echo ""  # Blank line
echo "ThirdStage completed."
echo ""  # Blank line
echo "------------------------------------------"

