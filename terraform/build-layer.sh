#!/bin/bash

# Build Docker image
docker build -t lambda-layer-builder .

# Run container and copy the ZIP file
docker run --rm -v "$(pwd):/output" lambda-layer-builder -c "cp /lambda-layer/lambda-layer.zip /output/" 