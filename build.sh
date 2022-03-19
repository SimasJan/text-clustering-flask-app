#!/bin/bash

# build docker image
docker build -t text-clustering-app .

echo "Docker image `text-clustering-app` built"

sleep 6
# run the docker image
docker run -d \
    --name text-clustering-app \
    -p 5000:5000 \
    text-clustering-app

echo "Docker container `text-clustering-app` running on port 5000"
