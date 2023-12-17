import json

import requests
from bs4 import BeautifulSoup


def lambda_handler(event, context):
    cafe_name = event.get("pathParameters", {}).get("id", None)

    if not cafe_name:
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

    result = []

    res = requests.get(
        f"https://cafe.naver.com/{cafe_name}",
        headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        },
    )
    soup = BeautifulSoup(res.text, 'html.parser')
    soup.prettify()

    els = soup.select(
        "ul.cafe-menu-list > li"
    )

    for i in els:
        cafe_menu_id = None
        print(i.select_one("a").get("href").split("menuid="))
        print(len(i.select_one("a").get("href").split("menuid=")))
        if len(i.select_one("a").get("href").split("menuid=")) > 1:
            cafe_menu_id = i.select_one("a").get("href").split(
                "menuid=")[1].split("&")[0]

        cafe_board_type = None
        if len(i.select_one("a").get("href").split("boardtype=")) > 1:
            cafe_board_type = i.select_one("a").get("href").split(
                "boardtype=")[1].split("&")[0]
        else:
            continue

        def get_title(text: str):
            text = text.replace("\n", "").replace(
                "\t", "").replace("  ", "").replace("  ", "").strip()
            return text

        result.append(
            {
                "cafe_name": cafe_name,
                "board_name": get_title(i.select_one("a").text),
                "cafe_id": i.select_one("a").get("href").split(
                    "clubid=")[1].split("&")[0],
                "cafe_menu_id": cafe_menu_id,
                "cafe_board_type": i.select_one("a").get("href").split(
                    "boardtype=")[1].split("&")[0],
            }
        )

    return {
        "statusCode": "200",
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        "body": json.dumps(result)
    }
