#!/bin/bash
set -eo pipefail

./update_config.sh

./update_policy.sh

./deploy_lambda.sh