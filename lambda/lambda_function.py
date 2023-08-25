"""
Github alerts publisher lambda function.

Calls the Github Alerts API URL to publish notifications to SNS topics.
"""
import logging
import os
import requests


GH_ALERTS_API_URL = os.getenv('GH_ALERTS_API_URL')

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    _logger.info(f'event: {event}')

    response = requests.post(f'{GH_ALERTS_API_URL}/notifications', timeout=10)

    _logger.info(
        f'POST /notifications response: {response.json()}, status_code: {response.status_code}'
    )

    return {
        'status_code': 200,
        'body': 'success'
    }
