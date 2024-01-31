#!/bin/bash

EB_EXTENSIONS_DIR=.ebextensions
LISTENER_CONFIG=../${EB_EXTENSIONS_DIR}/securelistener-alb.config
LISTENER_CONFIG_TEMPLATE=../${EB_EXTENSIONS_DIR}/securelistener-alb.config.template

# Load environment variables
export $(cat ../.env | xargs)

# Populate envs into policy file
envsubst < $LISTENER_CONFIG_TEMPLATE > $LISTENER_CONFIG

eb deploy
