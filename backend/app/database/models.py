from sqlalchemy import Column, String, Integer, DateTime, JSON, ForeignKey, BOOLEAN, func, VARCHAR, VARCHAR, DATE
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import INTEGER
from app.database.database import Base


class Channel(Base):
    __tablename__ = "channel"

    id = Column(
        INTEGER(unsigned=True),
        primary_key=True,
        index=True,
        comment="채널 고유번호"
    )
    panel_title = Column(
        VARCHAR(255),
        nullable=False,
        default="Naver Cafe",
        comment="패널에 보일 제목"
    )
    cafe_name = Column(
        VARCHAR(255),
        nullable=False,
        default="",
        comment="카페 이름"
    )
    cafe_id = Column(
        VARCHAR(255),
        nullable=False,
        default="",
        comment="카페 고유번호"
    )
    cafe_menu_id = Column(
        VARCHAR(255),
        nullable=False,
        default="",
        comment="카페 메뉴 고유번호"
    )
    cafe_board_type = Column(
        VARCHAR(255),
        nullable=False,
        default="L",
        comment="카페 게시판 타입"
    )
