#!/bin/bash

REQUIREMENTS_FILE=requirements_deploy.txt

FUNCTION_NAME=gh-alerts-publisher

rm -rf package
rm deployment-package.zip

mkdir package
echo 'Installing lambda-specific dependencies...'
pip install --upgrade pip
pip install --platform manylinux_2_24_x86_64 --target=./venv/lib/python3.9/site-packages --implementation cp --python-version 3.9 --only-binary=:all: --target ./package -r  ../$REQUIREMENTS_FILE
cd package
zip -qr ../deployment-package.zip .
cd ..

echo "Deploying lambda function: ${FUNCTION_NAME}"
cd ..   # Need to be in same dir as the lambda function for the zip to work...
zip -g scripts/deployment-package.zip lambda_function.py
aws lambda update-function-code --function-name $FUNCTION_NAME --zip-file fileb://scripts/deployment-package.zip