# Github Alerts

_This App is a work in progress!_ Stay tuned :sparkles:

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
