#!/bin/bash

CURR_DIR="$(dirname "$(realpath "$0")")"

call_script() {
    bash "$CURR_DIR/generate_and_upload.sh"
    return $?
}

echo "caller_script started, current time is: $(date)"
RANDOM_DELAY=$((RANDOM % 18000))
echo "sleeping for $RANDOM_DELAY"
sleep $RANDOM_DELAY
echo "done sleeping, current time is: $(date)"

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
