"""
DynamoDB helpers
"""
from dataclasses import dataclass
import logging
import boto3


_logger = logging.getLogger(__name__)


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

    def get_attr_dict(self):
        """Converts attribute field-values into a dictionary"""
        attrs = {}
        for field in self.__dataclass_fields__:
            value = getattr(self, field)
            attrs[field] = value

        return attrs


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

    def update_user(self, username, user_data: UserData, allow_none):
        """Update user field"""
        update_exp_list = []
        exp_attr_vals_dict = {}

        for key, value in user_data.get_attr_dict().items():
            if key == 'username' or (not allow_none and not value):
                continue
            update_exp_list.append(f'{key} = :{key}')
            exp_attr_vals_dict[f':{key}'] = value

        update_exp = f'SET {",".join(update_exp_list)}'

        response = self.table.update_item(
            Key={'username': username},
            UpdateExpression=update_exp,
            ExpressionAttributeValues=exp_attr_vals_dict
        )
        return response

    def write_data(self, data):
        """Add any data to table"""
        with self.table.batch_writer() as batch:
            batch.put_item(Item=data)
