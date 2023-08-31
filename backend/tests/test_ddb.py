"""
Tests for GH Alerts Users class & methods
"""
import logging
import os
from dotenv import load_dotenv
from moto import mock_dynamodb
import pytest
from helpers.ddb import create_users_table, GHAlertsUsersTable, UserData


load_dotenv()
AWS_REGION = os.getenv('AWS_REGION')
GH_ALERTS_USERS_TABLE_NAME = os.getenv('GH_ALERTS_USERS_TABLE_NAME')
MOCK_DATA = {
    'username': 'test',
    'sns_subscriptions': [],
    'webhooks': [],
    'tracking_repos': '*',
    'scheduled_alerts': False,
    'live_pr_alerts': False
}

_logger = logging.getLogger(__name__)


def _create_mock_table():
    """Create a mock table"""
    create_users_table(GH_ALERTS_USERS_TABLE_NAME, AWS_REGION)
    table = GHAlertsUsersTable(GH_ALERTS_USERS_TABLE_NAME, AWS_REGION)
    table.write_data(MOCK_DATA)
    return table


@mock_dynamodb
@pytest.mark.parametrize(
    'username, sns_subscriptions, webhooks, tracking_repos, scheduled_alerts, \
        live_pr_alerts, expected_user',
    [
        (
            'naomiven', [{'protocol': 'email', 'endpoint': 'hi@naomi.com'}, \
                {'protocol': 'sms', 'endpoint': '12345678900'}], \
                [{'name': 'ms_teams', 'url': 'http://fake-ms-teams-webhook-url.com'},
                {'name': 'slack','url': 'http://fake-slack-webhook-url.com'}], '*', True, True,
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
                    {
                        'name': 'ms_teams',
                        'url': 'http://fake-ms-teams-webhook-url.com'
                    },
                    {
                        'name': 'slack',
                        'url': 'http://fake-slack-webhook-url.com'
                    }
                ],
                'tracking_repos': '*',
                'scheduled_alerts': True,
                'live_pr_alerts': True
            }
        )
    ]
)
# pylint: disable=too-many-arguments
def test_create_user(
    username, sns_subscriptions, webhooks, tracking_repos, scheduled_alerts, \
    live_pr_alerts, expected_user
):
    """Test create user to a mock table"""
    table = _create_mock_table()

    user_data = UserData(
        username=username,
        sns_subscriptions=sns_subscriptions,
        webhooks=webhooks,
        tracking_repos=tracking_repos,
        scheduled_alerts=scheduled_alerts,
        live_pr_alerts=live_pr_alerts
    )

    response = table.create_user(user_data)
    _logger.debug(response)

    assert response['ResponseMetadata']['HTTPStatusCode'] == 200

    retrieve_response = table.get_user('naomiven')
    _logger.debug(f'retrieve_response: {retrieve_response}')

    assert retrieve_response == expected_user


@mock_dynamodb
@pytest.mark.parametrize(
    'username, exists',
    [
        ('test', True),
        ('i-do-not-exist', False)
    ]
)
def test_get_user(username, exists):
    """Test get user"""
    table = _create_mock_table()

    response = table.get_user(username)
    _logger.debug(f'get_user response: {response}')

    if exists:
        assert all(field in response for field in [
            'username', 'sns_subscriptions', 'webhooks', 'tracking_repos', \
            'scheduled_alerts', 'live_pr_alerts'
        ])
    else:
        assert not response


@mock_dynamodb
@pytest.mark.parametrize(
    'username, user_data, allow_none, expected',
    [
        (
            'test',
            UserData(
                sns_subscriptions=[{'protocol': 'email', 'endpoint': 'test@naomi.com'}],
                webhooks=[{'name': 'ms_teams', 'url': 'http://fake-ms-teams-webhook-url.com'}],
                tracking_repos='*',
                scheduled_alerts=True,
                live_pr_alerts=True
            ),
            True,
            {
                'username': 'test',
                'sns_subscriptions': [{'protocol': 'email', 'endpoint': 'test@naomi.com'}],
                'webhooks': [{'name': 'ms_teams', 'url': 'http://fake-ms-teams-webhook-url.com'}],
                'tracking_repos': '*',
                'scheduled_alerts': True,
                'live_pr_alerts': True
            }
        ),
        (
            'test',
            UserData(scheduled_alerts=True),
            False,
            {
                'username': 'test',
                'sns_subscriptions': [],
                'webhooks': [],
                'tracking_repos': '*',
                'scheduled_alerts': True,   # Only this one changed
                'live_pr_alerts': False
            }
        )
    ]
)
def test_update_user(username, user_data, allow_none, expected):
    """Test update user"""
    table = _create_mock_table()

    response = table.update_user(username, user_data, allow_none)
    assert response['ResponseMetadata']['HTTPStatusCode'] == 200

    response = table.get_user(username)
    assert response == expected
