import json

def lambda_handler(event, context):
    print('TESTING')
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
