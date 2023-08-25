# Github Alerts

_This App is a work in progress!_ Stay tuned :sparkles:

Technology used:

**Backend**: Python, Flask, AWS (SMS, SNS, EC2, Lambda, EventBridge), MS Teams Webhook

**Frontend**: _TBD_

## Backend

### Test locally

Install dependencies

```python3
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -r requirements-test.txt
```

Run app

```sh
flask --app app --debug run
```

In a new terminal

```sh
curl http://localhost:5000/
> Welcome to Naomi's app :D
```

### Deploy

#### Create a new applciation

```sh
eb init -p python-3.9 gh-alerts --region <app-region>

# Configure a default keypair in order to connect to the EC2 instance that hosts your app
eb init

# Create environment and deploy
eb create gh-alerts

# Set environment variables
cd scripts
./set_envs.sh
```

In configuration settings, ensure that the EC2 instance profile points to the IAM role `gh-alerts-role` and WSGI Path is set to `app:app`

#### Deploy to an existing application

```sh
eb deploy
```

### Deploy Lambda function

```sh
cd <root-dir>/lambda/scripts
./deploy.sh
```

## AWS Scripts

`set_envs.sh`: Sets the environment variables for the backend in Elastic Beanstalk.

`update_policy.sh`: Updates the IAM policy (attached to IAM role) of the backend's EC2 instance profile. This policy contains permissions for accessing specific AWS resources.

## Lambda Scripts

The `deploy.sh` script executes the steps below in order:

1. `update_config.sh`: Updates the lambda function's environment variables
2. `deploy_lambda.sh`: Installs dependencies and deploys the lambda function

### EventBridge Scheduled Events

Trigger the lambda at a scheduled rate using EventBridge Scheduler. To trigger every hour from 9:00 - 17:00, Monday to Friday, use cron expression:

```sh
0 9-17 ? * MON-FRI *
```
