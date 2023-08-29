"""
Tests for GH Alerts Users class & methods
"""
import logging
import os
from moto import mock_dynamodb
import pytest
from helpers.ddb import create_users_table, GHAlertsUsersTable, UserData



APP_REGION = os.getenv('APP_REGION')
GH_ALERTS_USERS_TABLE_NAME = os.getenv('GH_ALERTS_USERS_TABLE_NAME')
MOCK_DATA = {
    'username': 'test',
    'sns_subscriptions': [],
    'webhooks': [],
    'receive_real_time_PR_alerts': True
}

_logger = logging.getLogger(__name__)


def _create_mock_table():
    """Create a mock table"""
    create_users_table(GH_ALERTS_USERS_TABLE_NAME, APP_REGION)
    table = GHAlertsUsersTable(GH_ALERTS_USERS_TABLE_NAME, APP_REGION)
    # table.write_data(MOCK_DATA)
    return table


@mock_dynamodb
@pytest.mark.parametrize(
    'username, sns_subscriptions, webhooks, tracking_repos, receive_scheduled_alerts, \
        receive_real_time_PR_alerts, expected_user',
    [
        (
            'naomiven', [{'protocol': 'email', 'endpoint': 'hi@naomi.com'}, \
                {'protocol': 'sms', 'endpoint': '12345678900'}], \
                ['http://fake-ms-teams-webhook-url.com', 'http://fake-slack-webhook-url.com'], \
                '*', True, True,
            {
                'username': 'naomiven',
                'sns_subscriptions': [
                    {
                        'protocol': 'email',
                        'endpoint': 'hi@naomi.com'
                    },
                    {
                        'protocol': 'sms',
                        'endpoint': '12345678900'
                    }
                ],
                'webhooks': [
                    'http://fake-ms-teams-webhook-url.com', 'http://fake-slack-webhook-url.com'
                ],
                'tracking_repos': '*',
                'receive_scheduled_alerts': True,
                'receive_real_time_PR_alerts': True
            }
        )
    ]
)
def test_create_user(
    user_email, sns_subscriptions, webhooks, tracking_repos, receive_scheduled_alerts, \
    receive_real_time_PR_alerts, expected_user
):
    """Test create user to a mock table"""
    table = _create_mock_table()

    # TODO this
    user_data = UserData()

    table.create_user(user_data)
    retrieve_response = table.get_user('naomiven')
    _logger.info(f'retrieve_response: {retrieve_response}')

    assert retrieve_response == expected_user
