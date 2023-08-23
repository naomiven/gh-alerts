# gh-alerts

```python3
pip install -U pip
pip install -r requirements-test.txt
```

Run app

```sh
flask --app app --debug run
```

## Creating a new application in Elastic Beanstalk

```sh
eb init -p python-3.9 gh-alerts --region us-west-2
```

Configure a default keypair so that you can connect to the EC2 instance that hosts your app

```sh
eb init
```

Create environment and deploy

```sh
eb create gh-alerts
```

## Deploying to an existing application

```sh
eb deploy
```
