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

    body = json.loads(event.get("body", "{}"))

    keys = ["panel_title", "cafe_name", "cafe_id",
            "cafe_menu_id", "cafe_board_type"]

    for key in keys:
        if key not in body:
            return {
                "statusCode": "400",
                "headers": {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                "body": json.dumps({
                    "message": f"'{key}' is required"
                })
            }

    dynamodb = boto3.resource(
        "dynamodb",
        region_name="ap-northeast-2"
    )

    table = dynamodb.Table("Channel")

    response = table.put_item(
        Item={
            "id": id,
            "panel_title": body["panel_title"],
            "cafe_name": body["cafe_name"],
            "cafe_id": body["cafe_id"],
            "cafe_menu_id": body["cafe_menu_id"],
            "cafe_board_type": body["cafe_board_type"]
        }
    )

    return {
        "statusCode": "200",
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        "body": json.dumps(response)
    }
