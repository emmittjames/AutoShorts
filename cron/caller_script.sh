#!/bin/bash

CURR_DIR="$(dirname "$(realpath "$0")")"

call_script() {
    bash "$CURR_DIR/generate_and_upload.sh"
    return $?
}

main() {
    attempts=0
    max_attempts=3

    while [ $attempts -lt $max_attempts ]; do
        echo "executing the script from caller"
        call_script

        if [ $? -eq 0 ]; then
            echo "script executed successfully"
            break
        else
            echo "script failed. retrying in 1 minute..."
        attempts=$((attempts + 1))
        fi

        sleep 60
    done

    if [ $attempts -eq $max_attempts ]; then
        echo "max attempts reached, exiting :("
    fi
}

echo "caller_script started, current time is: $(date)"

RANDOM_CHOICE=$((RANDOM % 100 + 1))
if [ $RANDOM_CHOICE -le 1 ]; then
    RUN_COUNT=2  # 1% chance
elif [ $RANDOM_CHOICE -le 98 ]; then
    RUN_COUNT=1  # 97% chance
else
    RUN_COUNT=0  # 2% chance
fi

echo "Determined RUN_COUNT for today: $RUN_COUNT"

for (( i=0; i<RUN_COUNT; i++ )); do
    RANDOM_DELAY=$((RANDOM % 10800))
    echo "sleeping for $RANDOM_DELAY seconds before run #$((i + 1))"
    sleep $RANDOM_DELAY
    echo "done sleeping, current time is: $(date)"
    main
    echo "run #$((i + 1)) finished, current time is: $(date)"
done

echo "all done :D, current time is: $(date)"
