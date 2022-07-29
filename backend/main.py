import flask
import requests
import json
import os
import pymysql

naver_api_config = {
    "X-Naver-Client-Id": os.environ["X-Naver-Client-Id"],
    "X-Naver-Client-Secret": os.environ["X-Naver-Client-Secret"]
}

mysql_config = {
    "username": os.environ["CLEARDB_DATABASE_URL"][8:22],
    "password": os.environ["CLEARDB_DATABASE_URL"][23:31],
    "host": os.environ["CLEARDB_DATABASE_URL"][32:59],
    "database": os.environ["CLEARDB_DATABASE_URL"][60:82],
    "port": 3306
}

app = flask.Flask(__name__)


@app.route('/', methods=["GET"])
def main():
    return "Hello World"


@app.route('/naver', methods=["GET"])
def naver():
    parameter = flask.request.args.to_dict()
    my_res = flask.Response()
    my_res.headers.add("Access-Control-Allow-Origin", "*")

    if parameter.get("channel_id") == None:
        my_res.set_data("Not Found channel_id")
        return my_res

    connect = pymysql.connect(host=mysql_config["host"],
                              port=mysql_config["port"],
                              user=mysql_config["username"],
                              passwd=mysql_config["password"],
                              db=mysql_config["database"],
                              charset='utf8'
                              )

    cur = connect.cursor()
    cur.execute(
        f"SELECT keyword FROM channel WHERE channel_id = '{parameter['channel_id']}'")

    result = cur.fetchone()

    # 만약 미리 지정된 키워드가 없으면
    if result == ():

        my_res.set_data({"result": "NoSuchChannel"})
        return my_res

    print(result)

    response = requests.get(f"https://openapi.naver.com/v1/search/cafearticle.json?query={result[0]}&sort=date&display=12", headers={
                            "X-Naver-Client-Id": naver_api_config['X-Naver-Client-Id'], "X-Naver-Client-Secret": naver_api_config['X-Naver-Client-Secret']})

    connect.close()

    my_res.set_data(((response.text).replace("<\/b>", "")).replace("<b>", ""))
    return my_res


@ app.route('/config', methods=["GET", "POST"])
def config():
    parameter = flask.request.args.to_dict()
    my_res = flask.Response()
    my_res.headers.add("Access-Control-Allow-Origin", "*")

    if parameter.get("channel_id") == None:
        my_res.set_data("Not Found channel_id")
        return my_res

    if not("title" in parameter.keys() and "keyword" in parameter.keys() and "channel_id" in parameter.keys()):
        my_res.set_data("error (모든 파라미터를 입력해주세요)")
        return my_res

    connect = pymysql.connect(host=mysql_config["host"],
                              port=mysql_config["port"],
                              user=mysql_config["username"],
                              passwd=mysql_config["password"],
                              db=mysql_config["database"],
                              charset='utf8'
                              )

    cur = connect.cursor()

    query = f"SELECT * FROM channel WHERE EXISTS (SELECT channel_id FROM channel WHERE channel_id = '{parameter['channel_id']}');"

    # 만약 값이 있으면 -> 기존값 업데이트
    if cur.execute(query):
        cur.execute(
            f"UPDATE channel SET title = '{parameter['title']}', keyword = '{parameter['keyword']}' WHERE channel_id = '{parameter['channel_id']}';")
    # 만약 값이 없으면 -> 값 새로 입력
    else:
        cur.execute(
            f"INSERT INTO channel (channel_id, title, keyword) VALUES ('{parameter['channel_id']}', '{parameter['title']}', '{parameter['keyword']}');")

    connect.commit()
    connect.close()

    my_res.set_data("succse")
    return my_res


@ app.route('/title', methods=["GET"])
def title():
    parameter = flask.request.args.to_dict()
    my_res = flask.Response()
    my_res.headers.add("Access-Control-Allow-Origin", "*")

    if parameter.get("channel_id") == None:
        my_res.set_data("Not Found channel_id")
        return my_res

    connect = pymysql.connect(host=mysql_config["host"],
                              port=mysql_config["port"],
                              user=mysql_config["username"],
                              passwd=mysql_config["password"],
                              db=mysql_config["database"],
                              charset='utf8'
                              )

    cur = connect.cursor()

    cur.execute(
        f"SELECT title FROM channel WHERE channel_id = '{parameter['channel_id']}'")

    result = cur.fetchone()
    connect.close()

    # 만약 값이 없으면 -> 기본값 출력
    if result == ():
        my_res.set_data("{\"title\" : \"Naver Cafe\"}")
        return my_res
    # 만약 값이 있으면
    else:
        my_res.set_data("{\"title\" : \"" + result[0] + "\"}")
        return my_res


@ app.route('/keyword', methods=["GET"])
def keyword():
    parameter = flask.request.args.to_dict()
    my_res = flask.Response()
    my_res.headers.add("Access-Control-Allow-Origin", "*")

    if parameter.get("channel_id") == None:
        my_res.set_data("Not Found channel_id")
        return my_res

    connect = pymysql.connect(host=mysql_config["host"],
                              port=mysql_config["port"],
                              user=mysql_config["username"],
                              passwd=mysql_config["password"],
                              db=mysql_config["database"],
                              charset='utf8'
                              )

    cur = connect.cursor()

    cur.execute(
        f"SELECT keyword FROM channel WHERE channel_id = '{parameter['channel_id']}'")

    result = cur.fetchone()
    connect.close()

   # 만약 값이 없으면 -> 기본값 출력
    if result == ():
        my_res.set_data("{\"keyword\" : \"\"}")
        return my_res
    # 만약 값이 있으면
    else:
        my_res.set_data("{\"keyword\" : \"" + result[0] + "\"}")
        return my_res


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
