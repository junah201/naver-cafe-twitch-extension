from datetime import datetime


def lambda_handler(event, context):
    return {
        "statusCode": "200",
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Allow-Headers': '*',
        },
        "body": f"Notification API (UTC: {datetime.utcnow().strftime('%Y.%m.%d %H:%M:%S')})"
    }
