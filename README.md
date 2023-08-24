# Github Alerts

_This App is a work in progress!_ Stay tuned :sparkles:

Technology used:

**Backend**: Python, Flask, AWS (SMS, SNS, EC2, Lambda, EventBridge)

**Frontend**: _TBD_

## Backend

Install dependencies

```python3
pip install -U pip
pip install -r requirements-test.txt
```

Run app

```sh
flask --app app --debug run
```

### Deploy

#### Create a new applciation

```sh
eb init -p python-3.9 gh-alerts --region us-west-2

# Configure a default keypair in order to connect to the EC2 instance that hosts your app
eb init

# Create environment and deploy
eb create gh-alerts
```

Ensure that WSGI Path is set to `app:app`

#### Deploy to an existing application

```sh
eb deploy
```

## AWS Scripts

`set_envs.sh`: Sets the environment variables for the backend in Elastic Beanstalk.

`update_policy.sh`: Updates the IAM policy of the EC2 instance profile of the backend. This policy contains permissions for accessing specific AWS resources.

## Lambda Scripts

Deploy lambda function:

```sh
cd lambda/scripts
./deploy.sh
```

This script will execute the steps below in order:

1. `update_config.sh`: Updates the lambda function's environment variables
2. `deploy_lambda.sh`: Installs dependencies and deploys the lambda function

### EventBridge Scheduled Events

Trigger the lambda at a scheduled rate using EventBridge Scheduler. To trigger every hour from 9:00 - 17:00, Monday to Friday, use cron expression:

```sh
0 9-17 ? * MON-FRI *
```
