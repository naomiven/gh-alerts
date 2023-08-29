"""
DynamoDB helpers
"""
from dataclasses import dataclass
import boto3


def create_users_table(table_name, region_name):
    """Create GH Alerts Users table"""
    dynamodb = boto3.resource('dynamodb', region_name=region_name)
    table = dynamodb.create_table(
        TableName = table_name,
        KeySchema = [
            {'AttributeName': 'username', 'KeyType': 'HASH'}],
        AttributeDefinitions = [
            {'AttributeName': 'username', 'AttributeType': 'S'}
        ],
        BillingMode = 'PAY_PER_REQUEST'
    )
    return table


@dataclass
class UserData:
    """GH Alerts user dataclass"""
    username: str = None
    sns_subscriptions: list = None
    webhooks: list = None
    tracking_repos: list = None
    scheduled_alerts: bool = None
    live_pr_alerts: bool = None


class GHAlertsUsersTable:
    """GH Alerts Users Table"""
    def __init__(self, table_name, region_name):
        self.table_name = table_name
        self.region_name = region_name
        self.table = boto3.resource('dynamodb', region_name=self.region_name).Table(self.table_name)

    def create_user(self, user_data: UserData):
        """Create user"""
        item = {
            'username': user_data.username,
            'sns_subscriptions': user_data.sns_subscriptions,
            'webhooks': user_data.webhooks,
            'tracking_repos': user_data.tracking_repos,
            'scheduled_alerts': user_data.scheduled_alerts,
            'live_pr_alerts': user_data.live_pr_alerts
        }
        response = self.table.put_item(Item=item)
        return response

    def get_user(self, username):
        """Get user"""
        response = self.table.get_item(Key={'username': username})
        return response.get('Item')

    def write_data(self, data):
        """Add any data to table"""
        with self.table.batch_writer() as batch:
            batch.put_item(Item=data)
