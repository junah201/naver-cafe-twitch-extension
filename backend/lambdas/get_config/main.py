import json

import boto3


def lambda_handler(event, context):
    id = event.get(["pathParameters"], {}).get("id", None)

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

    return {
        "statusCode": "200",
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        "body": json.dumps(response["Item"])
    }
