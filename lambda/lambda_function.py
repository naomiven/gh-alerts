"""
Github alerts publisher lambda function.

Calls the Github Alerts API URL to publish notifications to SNS topics.
"""
import logging
import os
from typing import List
import boto3
import requests


GH_ALERTS_API_URL = os.getenv('GH_ALERTS_API_URL')
GH_ALERTS_USERS_TABLE_NAME = os.getenv('GH_ALERTS_USERS_TABLE_NAME')
MS_TEAMS_WEBHOOK_NAME = 'ms_teams'
REGION_NAME = os.getenv('REGION_NAME')

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)

table = boto3.resource('dynamodb', region_name=REGION_NAME).Table(GH_ALERTS_USERS_TABLE_NAME)


def _get_webhook_urls(users: dict) -> List:
    ms_teams_webhook_urls = []

    for user in users:
        ms_teams_webhook_url = next(
            (
                webhook['url'] for webhook in user['webhooks']
                if webhook['name'] == MS_TEAMS_WEBHOOK_NAME
            ), None
        )

        ms_teams_webhook_urls.append(ms_teams_webhook_url)

    return ms_teams_webhook_urls


def lambda_handler(event, context):
    _logger.info(f'event: {event}')

    response = table.scan()
    users = response['Items']
    _logger.debug(f'users: {users}')

    ms_teams_webhook_urls = _get_webhook_urls(users)

    json_body = {
        'ms_teams_webhook_urls': ms_teams_webhook_urls
    }

    _logger.debug(f'json_body: {json_body}')

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
