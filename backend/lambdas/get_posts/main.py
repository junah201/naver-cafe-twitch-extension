import json
from datetime import datetime
import requests

import boto3
from bs4 import BeautifulSoup


def lambda_handler(event, context):
    id = event.get("pathParameters", {}).get("id", None)

    if not id:
        return {
            "statusCode": "400",
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': 'true',
                'Access-Control-Allow-Methods': '*',
                'Access-Control-Allow-Headers': '*',
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
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': 'true',
                'Access-Control-Allow-Methods': '*',
                'Access-Control-Allow-Headers': '*',
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
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': 'true',
                'Access-Control-Allow-Methods': '*',
                'Access-Control-Allow-Headers': '*',
            },
            "body": json.dumps({
                "message": "Channel not found"
            })
        }

    item = response["Item"]

    result = []

    res = requests.get(
        "https://cafe.naver.com/ArticleList.nhn",
        params={
            'search.clubid': item["cafe_id"],
            'search.menuid': item["cafe_menu_id"],
            'search.boardtype': item["cafe_board_type"],
        },
    )
    soup = BeautifulSoup(res.text, 'html.parser')
    soup.prettify()

    table_els = soup.select("#main-area > div.article-board.m-tcol-c")
    els = table_els[1].select(
        "div.article-board > table > tbody > tr")

    def get_title(text: str):
        text = text.replace("\n", "").replace(
            "\t", "").replace("  ", "")
        return text

    for i in els:
        result.append(
            {
                "title": get_title(i.select_one(
                    "td.td_article > div.board-list > div > a.article").text),
                "link": f"https://cafe.naver.com{i.select_one('td.td_article > div.board-list > div > a.article').get('href')}",
                "writer": get_title(i.select_one(
                    'td.td_name > div.pers_nick_area').text),
                "date": f"{datetime.now().strftime('%Y.%m.%d')} {i.select_one('td.td_date').text}"
            }
        )

    return {
        "statusCode": "200",
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Allow-Headers': '*',
        },
        "body": json.dumps(result)
    }
