#!/bin/bash

# Prompt the user to enter the experiment name
echo "Enter the experiment name:"
read experimentName
echo ""

echo "Enter the club (club):"
read club
echo ""

# Directory where the stages are located (same level as main.sh)
directory=$(dirname "$0")


# Iterate over the directories at the same level as main.sh
for stage in "$directory"/*/; do
    stageName=$(basename "$stage")

    # Check if it is a valid stage directory (does not start with "_")
    if [[ $stageName != _* && -f "$stage/main_$stageName.sh" ]]; then

        bash "$stage/main_$stageName.sh" "$experimentName" "$club"
        echo ""
    fi
done
