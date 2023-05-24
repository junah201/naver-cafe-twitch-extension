from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import get_db, engine
from app.database import models, schemas
from sqlalchemy.orm import Session
import datetime
from typing import Optional, List
import aiohttp
from bs4 import BeautifulSoup

models.Base.metadata.create_all(bind=engine, checkfirst=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return f"Notification API (UTC: {datetime.datetime.utcnow().strftime('%Y.%m.%d %H:%M:%S')})"


@app.get("/{id}/config", response_model=schemas.Channel)
async def get_config(id: str, db: Session = Depends(get_db)):
    db_channel: Optional[models.Channel] = db.query(models.Channel).filter(
        models.Channel.id == id).first()

    if not db_channel:
        db_channel = models.Channel(id=id)
        db.add(db_channel)
        db.commit()

    return db_channel


@app.post("/{id}/config", response_model=schemas.Channel)
async def post_config(id: str, channel: schemas.ChannelUpdate, db: Session = Depends(get_db)):
    db_channel: Optional[models.Channel] = db.query(models.Channel).filter(
        models.Channel.id == id).first()

    if not db_channel:
        db_channel = models.Channel(id=id)
        db.add(db_channel)
        db.commit()

    db_channel.panel_title = channel.panel_title
    db_channel.cafe_name = channel.cafe_name
    db_channel.cafe_id = channel.cafe_id
    db_channel.cafe_menu_id = channel.cafe_menu_id
    db_channel.cafe_board_type = channel.cafe_board_type

    db.commit()

    return db_channel


@app.get("/{id}/posts", response_model=List[schemas.Post])
async def get_posts(id: str, db: Session = Depends(get_db)):
    db_channel: Optional[models.Channel] = db.query(models.Channel).filter(
        models.Channel.id == id).first()

    if not db_channel:
        raise HTTPException(
            status_code=404, detail="Channel not found"
        )

    result: List[schemas.Post] = []

    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(),
        headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36', },
        trust_env=True
    ) as session:
        async with session.get(
            "https://cafe.naver.com/ArticleList.nhn",
            params={
                'search.clubid': db_channel.cafe_id,
                'search.menuid': db_channel.cafe_menu_id,
                'search.boardtype': db_channel.cafe_board_type,
            },
        ) as response:
            html = await response.text()

            soup = BeautifulSoup(html, 'html.parser')
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
                    schemas.Post(
                        title=get_title(i.select_one(
                            "td.td_article > div.board-list > div > a.article").text),
                        link=f"https://cafe.naver.com{i.select_one('td.td_article > div.board-list > div > a.article').get('href')}",
                        writer=get_title(i.select_one(
                            'td.td_name > div.pers_nick_area').text),
                        date=f"{datetime.datetime.now().strftime('%Y.%m.%d')} {i.select_one('td.td_date').text}"
                    )
                )

    return result


@app.get("/{cafe_name}/boards", response_model=List[schemas.Board])
async def get_boards(cafe_name: str):
    result: List[schemas.Board] = []

    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(),
        headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36', },
        trust_env=True
    ) as session:
        async with session.get(
            f"https://cafe.naver.com/{cafe_name}",
        ) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
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
                    schemas.Board(
                        cafe_name=cafe_name,
                        board_name=get_title(i.select_one("a").text),
                        cafe_id=i.select_one("a").get("href").split(
                            "clubid=")[1].split("&")[0],
                        cafe_menu_id=cafe_menu_id,
                        cafe_board_type=i.select_one("a").get("href").split(
                            "boardtype=")[1].split("&")[0],
                    )
                )

        return result
