import logging
import os
from flask import Flask
from github import Auth, Github


AWS_REGION = os.getenv('AWS_REGION')
GH_NOTIF_ALERTS_SNS_TOPIC_ARN = os.getenv('GH_NOTIF_ALERTS_SNS_TOPIC_ARN')
GH_PR_ALERTS_SNS_TOPIC_ARN = os.getenv('GH_PR_ALERTS_SNS_TOPIC_ARN')
GH_TOKEN = os.getenv('GH_TOKEN')

logging.basicConfig(level=logging.DEBUG)

auth = Auth.Token(GH_TOKEN)
g = Github(auth=auth)

app = Flask(__name__)
app.logger.setLevel(logging.INFO)


@app.route('/')
def root():
    return 'Welcome to Naomi\'s app :D'
