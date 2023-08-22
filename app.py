import logging
import os
import boto3
from flask import Flask, request
from github import Auth, Github
from helpers.formatters import format_email_message, format_sms_message


AWS_REGION = os.getenv('AWS_REGION')
GH_EMAIL_ALERTS_SNS_TOPIC_ARN = os.getenv('GH_EMAIL_ALERTS_SNS_TOPIC_ARN')
GH_SMS_ALERTS_SNS_TOPIC_ARN = os.getenv('GH_SMS_ALERTS_SNS_TOPIC_ARN')
GH_TOKEN = os.getenv('GH_TOKEN')

logging.basicConfig(level=logging.DEBUG)

auth = Auth.Token(GH_TOKEN)
g = Github(auth=auth)

app = Flask(__name__)
app.logger.setLevel(logging.INFO)


class SNSPublisher:
    sns = boto3.resource('sns', region_name=AWS_REGION)
    email_topic = sns.Topic(GH_EMAIL_ALERTS_SNS_TOPIC_ARN)
    sms_topic = sns.Topic(GH_SMS_ALERTS_SNS_TOPIC_ARN)


    def publish(self, topic, subject, message):
        topic.publish(Subject=subject, Message=message)


    def publish_to_email_topic(self, subject, message):
        self.publish(self.email_topic, subject, message)


    def publish_to_sms_topic(self, subject, message):
        self.publish(self.sms_topic, subject, message)


class SNSSubscriber:
    client = boto3.client('sns', region_name=AWS_REGION)

    def subscribe_email(self, email):
        return self.client.subscribe(
            TopicArn=GH_EMAIL_ALERTS_SNS_TOPIC_ARN, Protocol='email', Endpoint=email
        )

    def subscribe_sms(self, phone_number):
        return self.client.subscribe(
            TopicArn=GH_SMS_ALERTS_SNS_TOPIC_ARN, Protocol='sms', Endpoint=phone_number
        )

    def get_subscribers(self, topic_arn):
        response = self.client.list_subscriptions_by_topic(TopicArn=topic_arn)

        subscriptions = response['Subscriptions']
        subscribers = [sub['Endpoint'] for sub in subscriptions]

        return subscribers

    def get_email_subscribers(self):
        return self.get_subscribers(GH_EMAIL_ALERTS_SNS_TOPIC_ARN)

    def get_sms_subscribers(self):
        return self.get_subscribers(GH_SMS_ALERTS_SNS_TOPIC_ARN)


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
    publisher.publish_to_email_topic(
        f'You have {len(messages)} unread Github notification{"s" if len(messages) > 1 else ""}', \
        message
    )

    message = format_sms_message(messages)
    publisher.publish_to_sms_topic('GH Alerts', message)

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

    email_subscribers = subscriber.get_email_subscribers()

    if email and email not in email_subscribers:
        response = subscriber.subscribe_email(email)
        status_code = response['ResponseMetadata']['HTTPStatusCode']

        if status_code != 200:
            return {'message': 'Cannot create email subscription'}, status_code

    sms_subscribers = subscriber.get_sms_subscribers()

    if phone_number and phone_number not in sms_subscribers:
        response = subscriber.subscribe_sms(phone_number)
        status_code = response['ResponseMetadata']['HTTPStatusCode']

        if status_code != 200:
            return {'message': 'Cannot create SMS subscription'}, status_code

    return {'message': 'success'}
