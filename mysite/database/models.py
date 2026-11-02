from .db import Base
from sqlalchemy import Integer, String, ForeignKey, DateTime, Text, Enum, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, date
from typing import List
from enum import Enum as PyEnum


class UserRole(str, PyEnum):
    admin = 'admin'
    visitor = 'visitor'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    username: Mapped[str] = mapped_column(String(32), unique=True)
    email: Mapped[str] = mapped_column(String(64), unique=True)
    password: Mapped[str] = mapped_column(String(256), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.visitor)
    date_registered: Mapped[date] = mapped_column(Date, default=date.today)
    user_token: Mapped[List['RefreshToken']] = relationship(back_populates='token_user',
                                                            cascade='all, delete-orphan')

    def __str__(self):
        return self.username


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    token_user: Mapped[User] = relationship(back_populates='user_token')
    token: Mapped[str] = mapped_column(String(512), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    def __str__(self):
        return f'{self.token_user}, {self.token}'


class Exhibit(Base):
    __tablename__ = 'exhibit'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    title: Mapped[str] = mapped_column(String(64))
    description: Mapped[str] = mapped_column(Text)
    history: Mapped[str] = mapped_column(Text)
    origin: Mapped[str] = mapped_column(String(128))
    image_url: Mapped[str] = mapped_column(String(256))

    def __str__(self):
        return self.title
