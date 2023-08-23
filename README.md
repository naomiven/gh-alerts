# Github Alerts

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
