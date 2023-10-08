#!/bin/bash

FUNCTION_NAME=gh-alerts-publisher
POLICY_FILE=policy.json
POLICY_FILE_TEMPLATE=policy.json.template
POLICY_NAME=gh-alerts-publisher-policy

role_arn=$(aws lambda get-function-configuration --function-name $FUNCTION_NAME --query 'Role' --output text)
echo "Role ARN: $role_arn"

role_regex="^arn:aws:iam::[0-9]+:role/service-role/(.+)"
if [[ $role_arn =~ $role_regex ]]; then
  role_name=${BASH_REMATCH[1]}
  echo "Role name: $role_name"
else
  echo "No match found for role name!"
  exit 1
fi

ROLE_NAME=$role_name

# Load environment variables
export $(cat ../.env | xargs)

# Populate envs into policy file
envsubst < $POLICY_FILE_TEMPLATE > $POLICY_FILE

# Get attached policy ARN from role
policy_arn=$(aws iam list-attached-role-policies --role-name "$ROLE_NAME" --query "AttachedPolicies[?PolicyName=='$POLICY_NAME'].PolicyArn | [0]" --output text)

if [[ "$policy_arn" != "None" ]]; then
    echo "Policy ARN: $policy_arn"
else
    echo "Policy $POLICY_NAME is not attached to the role $ROLE_NAME"
    exit 1
fi

# Create policy ARN version
echo 'Creating policy version...'
aws iam create-policy-version --policy-arn $policy_arn --policy-document file://$POLICY_FILE --set-as-default

if [[ $? = 254 ]]
then
  # Must delete a policy version first
  version_to_delete=$(aws iam list-policy-versions --policy-arn $policy_arn --query 'Versions[-1:].VersionId' --output text)
  echo "Deleting version: $version_to_delete"

  aws iam delete-policy-version --policy-arn $policy_arn --version-id $version_to_delete

  # Create policy ARN version
  echo 'Creating policy version...'
  aws iam create-policy-version --policy-arn $policy_arn --policy-document file://$POLICY_FILE --set-as-default
fi