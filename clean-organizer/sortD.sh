#!/bin/bash

# Function to run a script
run_script() {
    local script_path=$1
    echo "Running $script_path"
    python3 "$script_path"
    if [ $? -ne 0 ]; then
        echo "Failed to run $script_path"
        exit 1
    else
        echo "Successfully ran $script_path"
    fi
}

# List of scripts to run
scripts=(
'/Users/steven/clean/clean-organizer/audio.py'
'/Users/steven/clean/clean-organizer/config.py'
'/Users/steven/clean/clean-organizer/docs.py'
'/Users/steven/clean/clean-organizer/img.py'
'/Users/steven/clean/clean-organizer/organize.py'
'/Users/steven/clean/clean-organizer/other.py'
'/Users/steven/clean/clean-organizer/vids.py'
)

# Run each script in the list
for script in "${scripts[@]}"; do
    run_script "$script"
done
