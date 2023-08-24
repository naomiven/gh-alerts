"""
Github alerts publisher lambda function.

Calls the Github Alerts API URL to publish notifications to SNS topics.
"""
import json
import logging
import os
import requests


GH_ALERTS_API_URL = os.getenv('GH_ALERTS_API_URL')

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    _logger.info('Hello!')

    response = requests.get(GH_ALERTS_API_URL, timeout=3)

    _logger.info(f'response: {response.content}')

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
