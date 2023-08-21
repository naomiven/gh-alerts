"""
Formatter functions
"""


def format_email_message(messages: list):
    formatted_messages = [
        f'"{message["title"]}" ({message["type"]}) by @{message["user"]} at {message["url"]}' \
        for message in messages
    ]

    return '\n'.join(formatted_messages)
