#!/bin/bash -e

# Function to execute a stage
execute_stage() {
    local stage="$1"
    local experimentName="$2"
    local club="$3"
    python "0Stage/startData.py" "$experimentName" "$stage"
    bash "$stage/main$stage.sh" "$experimentName" "$club"
}

# Function to handle errors
handle_error() {
    local stage="$1"
    echo "Error in main$stage.sh. Execution ended."
    exit 1
}

# Main function
main() {
    echo "------------------------------------------"
    read -p "Enter the experiment name: " experimentName
    echo ""
    read -p "Enter the club: " club
    echo ""

    directory=$(dirname "$0")
    mistakeGenerated=false

    for stage in "$directory"/*/; do
        stageName=$(basename "$stage")

        if [[ $stageName != _* && -f "$stage/main$stageName.sh" ]]; then
            execute_stage "$stageName" "$experimentName" "$club" || handle_error "$stageName"
            echo ""
        fi
    done

    echo "All executed correctly"
}

# Entry point
main "$@"
