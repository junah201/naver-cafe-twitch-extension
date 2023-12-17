from datetime import datetime

def lambda_handler(event, context):
    return {
        "statusCode": "200",
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        "body": f"Notification API (UTC: {datetime.utcnow().strftime('%Y.%m.%d %H:%M:%S')})"
    }
