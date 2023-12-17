import json

import boto3


def lambda_handler(event, context):
    id = event.get("pathParameters", {}).get("id", None)

    if not id:
        return {
            "statusCode": "400",
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps({
                "message": "'id' is required"
            })
        }

    try:
        id = int(id)
    except ValueError:
        return {
            "statusCode": "400",
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps({
                "message": "'id' must be number"
            })
        }

    dynamodb = boto3.resource(
        "dynamodb",
        region_name="ap-northeast-2"
    )

    table = dynamodb.Table("Channel")

    response = table.get_item(
        Key={
            "id": id
        }
    )

    if "Item" not in response:
        return {
            "statusCode": "404",
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps({
                "message": "Channel not found"
            })
        }

    item = {
        key: str(value) if isinstance(value, str) else int(value)
        for key, value in response["Item"].items()
    }

    return {
        "statusCode": "200",
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        "body": json.dumps(item)
    }
