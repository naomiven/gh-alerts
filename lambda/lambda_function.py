"""
Github alerts publisher lambda function.

Calls the Github Alerts API URL to publish notifications to SNS topics.
"""
import logging
import os
import boto3
import requests


GH_ALERTS_API_URL = os.getenv('GH_ALERTS_API_URL')

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)

client = boto3.client('dynamodb')


def lambda_handler(event, context):
    _logger.info(f'event: {event}')

    response = client.scan()
    users = response['Items']
    _logger.info(f'users: {users}')

    ms_teams_webhook_urls = []

    for user in users:
        ms_teams_webhook_url = next(
            (webhook['url'] for webhook in user['webhooks'] if webhook['name'] == 'ms_teams'), None
        )

        ms_teams_webhook_urls.append(ms_teams_webhook_url)


    json_body = {
        'ms_teams_webhook_urls': ms_teams_webhook_urls
    }

    response = requests.post(
        f'{GH_ALERTS_API_URL}/notifications', json=json_body, timeout=10
    )

    _logger.info(
        f'POST /notifications response: {response.json()}, status_code: {response.status_code}'
    )

    return {
        'status_code': 200,
        'body': 'success'
    }
