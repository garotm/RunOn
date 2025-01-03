#!/bin/bash

# Load environment variables from .env file
if [ -f ../../.env ]; then
    export $(cat ../../.env | grep -v '^#' | xargs)
fi

# Create temporary xcconfig file
echo "GOOGLE_CLIENT_ID_ENV = $RUNON_CLIENT_ID" > ../tmp.xcconfig 