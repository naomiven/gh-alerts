"""
Test helper functions
"""
import logging
from helpers.formatters import format_email_message, format_sms_message


_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)


def test_format_email_message():
    messages = [
        {
            'title': 'Notification Title',
            'url': 'https://github.com/',
            'user': 'naomiven',
            'type': 'PullRequest'
        }
    ]

    expected = '"Notification Title" (PullRequest) by @naomiven at https://github.com/'

    formatted = format_email_message(messages)

    assert formatted == expected


def test_format_sms_message():
    messages = [
        {
            'title': 'Notification Title',
            'url': 'https://github.com/',
            'user': 'naomiven',
            'type': 'PullRequest'
        }
    ]

    expected = 'GH Alerts > You have 1 unread Github notification.\n\n' + \
        '"Notification Title" (PullRequest) by @naomiven\n\n' + \
        'For more details, visit https://github.com/notifications'

    formatted = format_sms_message(messages)

    assert formatted == expected
