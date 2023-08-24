#!/bin/bash

FUNCTION_NAME=gh-alerts-publisher
CONFIG_FILE=config.json
CONFIG_FILE_TEMPLATE=config.json.template

# Load environment variables
export $(cat ../.env | xargs)

# Populate envs into config file
envsubst < $CONFIG_FILE_TEMPLATE > $CONFIG_FILE

# Get Lambda environment variables from config
envs=$( jq -s '.[0].environment_variables' config.json config.json )

# Map envs to key=value format
formatted_envs=$(jq -r 'to_entries | map("\(.key)=\(.value|tostring),") | .[]' <<< "${envs}")
echo "Variables={${formatted_envs}}"

echo "Updating environment variables for $FUNCTION_NAME"
aws lambda update-function-configuration --function-name $FUNCTION_NAME --environment "Variables={$formatted_envs}"