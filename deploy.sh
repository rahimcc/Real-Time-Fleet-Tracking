#!/bin/bash

set -e


echo "Pulling latest code" 
git pull 

echo "Stopping current container" 
docker stop fleet-tracker

echo "Deleting current container" 
docker rm fleet-tracker

echo "Running new container" 
docker run -d -p 8000:8000 --name fleet-tracker --restart unless-stopped fleet-tracker