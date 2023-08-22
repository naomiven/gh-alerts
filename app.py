import logging
import os
import boto3
from flask import Flask, request
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


class SNSSubscriber:
    client = boto3.client('sns', region_name=AWS_REGION)

    def subscribe(self, protocol, endpoint):
        return self.client.subscribe(
            TopicArn=GH_NOTIF_ALERTS_SNS_TOPIC_ARN, Protocol=protocol, Endpoint=endpoint
        )


publisher = SNSPublisher()
subscriber = SNSSubscriber()


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
            url = issue.html_url
            user = issue.user.login
        elif notif.subject.type == 'PullRequest':
            pr = notif.get_pull_request()
            url = pr.html_url
            user = pr.user.login
        else:
            user = '<unknown-user>'
            url = '<unknown-url>'

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
        f'You have {len(messages)} unread Github notification{"s" if len(messages) > 1 else ""}', \
        message
    )

    return {'message': 'success'}


@app.route('/pull-requests', methods=['GET'])
def publish_unread_prs():
    current_user = g.get_user()
    notifications = current_user.get_notifications()
    messages = []

    for notif in notifications:
        if notif.subject.type != 'PullRequest':
            continue

        pr = notif.get_pull_request()
        url = pr.html_url
        reviewers = pr.requested_reviewers
        user = pr.user.login

        if current_user.login not in [reviewer.login for reviewer in reviewers]:
            continue

        messages.append(
            {
                'title': notif.subject.title,
                'url': url,
                'user': user,
                'type': notif.subject.type
            }
        )

    app.logger.info(f'messages: {messages}')

    if len(messages) == 0:
        return {'message': 'No PRs to review!'}

    # TODO: publish

    return {'message': 'success'}


@app.route('/subscriptions', methods=['POST'])
def subscribe():
    email = request.json.get('email')
    phone_number = request.json.get('phone_number')

    if not email and not phone_number:
        return {'message': 'Email or phone number required for subscription'}, 400

    if email:
        response = subscriber.subscribe('email', email)
        status_code = response['ResponseMetadata']['HTTPStatusCode']

        if status_code != 200:
            return {'message': 'Cannot create email subscription'}, status_code


    if phone_number:
        response = subscriber.subscribe('sms', phone_number)
        status_code = response['ResponseMetadata']['HTTPStatusCode']

        if status_code != 200:
            return {'message': 'Cannot create SMS subscription'}, status_code

    return {'message': 'success'}
