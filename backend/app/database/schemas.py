from pydantic import BaseModel, validator, EmailStr, constr
from typing import Optional


class ChannelCreate(BaseModel):
    id: int


class ChannelUpdate(BaseModel):
    panel_title: str
    cafe_name: str
    cafe_id: str
    cafe_menu_id: str
    cafe_board_type: str


class Channel(ChannelCreate, ChannelUpdate):
    class Config:
        orm_mode = True


class Post(BaseModel):
    title: str
    link: str
    writer: str
    date: str


class Board(BaseModel):
    cafe_name: str
    board_name: str
    cafe_id: str
    cafe_menu_id: Optional[str] = None
    cafe_board_type: str
