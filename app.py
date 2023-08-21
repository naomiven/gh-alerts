import logging
import os
import boto3
from flask import Flask
from github import Auth, Github
from helpers.formatters import format_email_message


AWS_REGION = os.getenv('AWS_REGION')
GH_NOTIF_ALERTS_SNS_TOPIC_ARN = os.getenv('GH_NOTIF_ALERTS_SNS_TOPIC_ARN')
GH_PR_ALERTS_SNS_TOPIC_ARN = os.getenv('GH_PR_ALERTS_SNS_TOPIC_ARN')
GH_TOKEN = os.getenv('GH_TOKEN')

logging.basicConfig(level=logging.DEBUG)

auth = Auth.Token(GH_TOKEN)
g = Github(auth=auth)

app = Flask(__name__)
app.logger.setLevel(logging.INFO)


class SNSPublisher:
    sns = boto3.resource('sns', region_name=AWS_REGION)
    notif_topic = sns.Topic(GH_NOTIF_ALERTS_SNS_TOPIC_ARN)
    pr_topic = sns.Topic(GH_PR_ALERTS_SNS_TOPIC_ARN)


    def publish(self, topic, subject, message):
        topic.publish(Subject=subject, Message=message)


    def publish_to_notif_topic(self, subject, message):
        self.publish(self.notif_topic, subject, message)


publisher = SNSPublisher()


@app.route('/')
def root():
    return 'Welcome to Naomi\'s app :D'


@app.route('/notifications', methods=['GET'])
def publish_unread_notifications():
    notifications = g.get_user().get_notifications()
    messages = []

    for notif in notifications:
        if notif.subject.type == 'Issue':
            issue = notif.get_issue()
            url = notif.get_issue().html_url
            user = issue.user.login
        elif notif.subject.type == 'PullRequest':
            pr = notif.get_pull_request()
            url = notif.get_pull_request().html_url
            user = pr.user.login
        else:
            user = '<Unknown User>'
            url = '<Unknown URL>'

        app.logger.info(notif.get_issue().html_url)

        messages.append(
            {
                'title': notif.subject.title,
                'url': url,
                'user': user,
                'type': notif.subject.type
            }
        )

    if len(messages) == 0:
        return {
            'message': 'No Github notifications!'
        }

    message = format_email_message(messages)

    publisher.publish_to_notif_topic(
        f'You have {len(messages)} unread Github notifications', message
    )

    return {
        'message': 'success'
    }
