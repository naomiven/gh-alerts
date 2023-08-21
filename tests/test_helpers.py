"""
Test helper functions
"""
import logging
from helpers.formatters import format_email_message


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
