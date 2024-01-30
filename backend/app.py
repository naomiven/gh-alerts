"""
Flask Backend App for Github Alerts
"""

import logging
import os
import boto3
from flask import Flask, request
from flask_cors import CORS
from github import Auth, Github
import requests
from helpers.ddb import GHAlertsUsersTable, UserData
from helpers.formatters import format_email_message, format_ms_teams_message, format_sms_message


AWS_REGION = os.getenv('AWS_REGION')
GH_ALERTS_USERS_TABLE_NAME = os.getenv('GH_ALERTS_USERS_TABLE_NAME')
GH_EMAIL_ALERTS_SNS_TOPIC_ARN = os.getenv('GH_EMAIL_ALERTS_SNS_TOPIC_ARN')
GH_SMS_ALERTS_SNS_TOPIC_ARN = os.getenv('GH_SMS_ALERTS_SNS_TOPIC_ARN')
GH_TOKEN = os.getenv('GH_TOKEN')
MS_TEAMS_INCOMING_WEBHOOK_URL = os.getenv('MS_TEAMS_INCOMING_WEBHOOK_URL')

logging.basicConfig(level=logging.INFO)

auth = Auth.Token(GH_TOKEN)
g = Github(auth=auth)
table = GHAlertsUsersTable(GH_ALERTS_USERS_TABLE_NAME, AWS_REGION)

app = Flask(__name__)ß
# TODO allow all origins for all routes for now, add specific allowed origins later
CORS(app, resources={r"/*": {"origins": "*"}})
app.logger.setLevel(logging.INFO)


class SNSPublisher:
    sns = boto3.resource('sns', region_name=AWS_REGION)
    email_topic = sns.Topic(GH_EMAIL_ALERTS_SNS_TOPIC_ARN)
    sms_topic = sns.Topic(GH_SMS_ALERTS_SNS_TOPIC_ARN)

    def publish(self, topic, subject, message):
        return topic.publish(Subject=subject, Message=message)

    def publish_to_email_topic(self, subject, message):
        return self.publish(self.email_topic, subject, message)

    def publish_to_sms_topic(self, subject, message):
        return self.publish(self.sms_topic, subject, message)


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
    response = publisher.publish_to_email_topic(
        f'You have {len(messages)} unread Github notification' + \
        f'{"s" if len(messages) > 1 else ""}',
        message
    )
    app.logger.debug(f'Publish to email topic response: {response}')

    message = format_sms_message(messages)
    response = publisher.publish_to_sms_topic('GH Alerts', message)
    app.logger.debug(f'Publish to SMS topic response: {response}')

    if request.json.get('ms_teams_webhook_urls'):
        for url in request.json['ms_teams_webhook_urls']:
            message = format_ms_teams_message(messages)
            response = requests.post(url, json=message, timeout=5)
            app.logger.debug(f'Publish to MS Teams Webhook response: {response.content}')

    # TODO post slack webhook URL

    return {'message': 'success'}


@app.route('/subscriptions', methods=['POST'])
def subscribe():
    email = request.json.get('email')
    phone_number = request.json.get('phoneNumber')

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


@app.route('/users/<username>')
def get_users(username):
    user = table.get_user(username)

    if user:
        return user

    return {'message': 'User not found'}, 404


@app.route('/users/<username>', methods=['PATCH'])
def update_user(username):
    sns_subscriptions = []
    webhooks = []

    if request.json.get('email'):
        sns_subscriptions.append({'protocol': 'email', 'endpoint': request.json['email']})

    if request.json.get('phoneNumber'):
        sns_subscriptions.append(
            {'protocol': 'phone_number', 'endpoint': request.json['phoneNumber']}
        )

    if request.json.get('msTeamsWebhookURL'):
        webhooks.append({'name': 'ms_teams', 'url': request.json['msTeamsWebhookURL']})

    if request.json.get('slackWebhookURL'):
        webhooks.append({'name': 'slack', 'url': request.json['slackWebhookURL']})

    user_data = UserData(
        sns_subscriptions=sns_subscriptions,
        webhooks=webhooks,
        tracking_repos=request.json.get('trackingRepos'),
        scheduled_alerts=request.json.get('scheduledAlerts'),
        live_pr_alerts=request.json.get('livePRAlerts')
    )

    table.update_user(username, user_data, True)

    return {'message': 'success'}
