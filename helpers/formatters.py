"""
Formatter functions
"""


def format_email_message(messages: list):
    formatted_messages = [
        f'"{message["title"]}" ({message["type"]}) by @{message["user"]} at {message["url"]}' \
        for message in messages
    ]

    return '\n'.join(formatted_messages)


def format_sms_message(messages: list):
    num_messages = len(messages)
    notifications = '\n'.join([
        f'"{message["title"]}" ({message["type"]}) by @{message["user"]}\n' \
        for message in messages
    ][:5])

    message = f'You have {num_messages if num_messages <= 10 else "10+"} unread Github ' + \
        f'notification{"s" if num_messages > 1 else ""}.\n\n' + \
        f'{notifications}\n' + \
        'For more details visit https://github.com/notifications' 

    return f'GH Alerts > {message}'
