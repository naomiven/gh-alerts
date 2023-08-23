#!/bin/bash

# Read the `.env` file and format it for the `eb setenv` command.
VARS=""
while IFS='=' read -r key value; do
    # Ensure that the key and value are non-empty.
    if [[ -n $key && -n $value ]]; then
        VARS="$VARS $key=$value"
    fi
done < ../.env

# Set environment variables
if [[ -n $VARS ]]; then
    eb setenv $VARS
else
    echo "No variables found in .env"
    exit 1
fi
