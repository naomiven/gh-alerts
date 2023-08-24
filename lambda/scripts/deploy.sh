#!/bin/bash
set -eo pipefail

./update_config.sh

./deploy_lambda.sh