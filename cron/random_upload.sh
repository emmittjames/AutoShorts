#!/bin/bash

set -e

echo "navigating to directory"
cd /home/emmitt/projects/autoshorts || exit

echo "activating venv"
source venv/bin/activate

echo "checking for active selenium container"
docker stop selenium || true
docker rm -f selenium || true

echo "starting selenium container"
docker run -d -p 4444:4444 -p 7900:7900 --shm-size="2g" --name selenium selenium/standalone-firefox:latest

echo "running main.py"
python main.py --upload

echo "stopping selenium container"
docker stop selenium

echo "removing selenium container"
docker rm -f selenium

echo "deactivating venv"
deactivate

echo "all done :)"
