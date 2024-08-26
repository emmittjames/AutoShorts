#!/bin/bash

call_script() {
    bash "./random_upload.sh"
    return $?
}

#RANDOM_DELAY=$((RANDOM % 18000))
RANDOM_DELAY=5
echo "sleeping for $RANDOM_DELAY"
sleep $RANDOM_DELAY

attempts=0
max_attempts=3

while [ $attempts -lt $max_attempts ]; do
    echo "executing the script from caller"
    call_script

    if [ $? -eq 0 ]; then
        echo "script executed successfully"
        break
    else
        echo "script failed. retrying in 2 minutes..."
	attempts=$((attempts + 1))
    fi

    sleep 120
done

if [ $attempts -eq $max_attempts ]; then
    echo "max attempts reached, exiting :("
fi
