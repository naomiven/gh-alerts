"""
Flask Backend App for Github Alerts
"""

import logging
import os
import boto3
from flask import Flask, request
from github import Auth, Github
import requests
from helpers.formatters import format_email_message, format_ms_teams_message, format_sms_message


AWS_REGION = os.getenv('AWS_REGION')
GH_EMAIL_ALERTS_SNS_TOPIC_ARN = os.getenv('GH_EMAIL_ALERTS_SNS_TOPIC_ARN')
GH_SMS_ALERTS_SNS_TOPIC_ARN = os.getenv('GH_SMS_ALERTS_SNS_TOPIC_ARN')
GH_TOKEN = os.getenv('GH_TOKEN')
MS_TEAMS_INCOMING_WEBHOOK_URL = os.getenv('MS_TEAMS_INCOMING_WEBHOOK_URL')

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

    def get_subscriptions(self, topic_arn):
        response = self.client.list_subscriptions_by_topic(TopicArn=topic_arn)

        return response['Subscriptions']

    def get_subscribers(self, topic_arn):
        subscriptions = self.get_subscriptions(topic_arn)
        subscribers = [sub['Endpoint'] for sub in subscriptions]

        return subscribers

    def get_email_subscribers(self):
        return self.get_subscribers(GH_EMAIL_ALERTS_SNS_TOPIC_ARN)

    def get_sms_subscribers(self):
        return self.get_subscribers(GH_SMS_ALERTS_SNS_TOPIC_ARN)

    def subscribe_email(self, email):
        return self.client.subscribe(
            TopicArn=GH_EMAIL_ALERTS_SNS_TOPIC_ARN, Protocol='email', Endpoint=email
        )

    def subscribe_sms(self, phone_number):
        return self.client.subscribe(
            TopicArn=GH_SMS_ALERTS_SNS_TOPIC_ARN, Protocol='sms', Endpoint=phone_number
        )

    def unsubscribe_email(self, email):
        subscriptions = self.get_subscriptions(GH_EMAIL_ALERTS_SNS_TOPIC_ARN)

        # Get SubscriptionArn
        sub_arn = next(
            (
                sub['SubscriptionArn'] for sub in subscriptions if sub['Endpoint'] == email
            ), None
        )

        if sub_arn:
            return self.client.unsubscribe(SubscriptionArn=sub_arn)

        return False

    def unsubscribe_sms(self, sms):
        subscriptions = self.get_subscriptions(GH_SMS_ALERTS_SNS_TOPIC_ARN)

        # Get SubscriptionArn
        sub_arn = next(
            (
                sub['SubscriptionArn'] for sub in subscriptions if sms in sub['Endpoint']
            ), None
        )

        if sub_arn:
            return self.client.unsubscribe(SubscriptionArn=sub_arn)

        return False


publisher = SNSPublisher()
subscriber = SNSSubscriber()


@app.route('/')
def root():
    return 'Welcome to Naomi\'s app :D'


@app.route('/notifications', methods=['POST'])
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
        f'You have {len(messages)} unread Github notification{"s" if len(messages) > 1 else ""}',
        message
    )

    message = format_sms_message(messages)
    publisher.publish_to_sms_topic('GH Alerts', message)

    message = format_ms_teams_message(messages)
    requests.post(MS_TEAMS_INCOMING_WEBHOOK_URL, json=message, timeout=3)

    return {'message': 'success'}


@app.route('/subscriptions', methods=['POST'])
def subscribe():
    email = request.json.get('email')
    phone_number = request.json.get('phone_number')

    if not email and not phone_number:
        return {'message': 'Email or phone number required for subscription'}, 400

    email_subscribers = subscriber.get_email_subscribers()

    if email and email not in email_subscribers:
        subscriber.subscribe_email(email)

    sms_subscribers = subscriber.get_sms_subscribers()

    if phone_number and phone_number not in sms_subscribers:
        subscriber.subscribe_sms(phone_number)

    return {'message': 'success'}


@app.route('/subscriptions', methods=['DELETE'])
def unsubscribe():
    email = request.json.get('email')
    phone_number = request.json.get('phone_number')

    if not email and not phone_number:
        return {'message': 'Email or phone number required for removing subscription'}, 400

    if email:
        subscriber.unsubscribe_email(email)

    if phone_number:
        subscriber.unsubscribe_sms(phone_number)

    return {'message': 'success'}
