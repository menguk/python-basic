"""
создайте алхимичный engine
добавьте declarative base (свяжите с engine)
создайте объект Session
добавьте модели User и Post, объявите поля:
для модели User обязательными являются name, username, email
для модели Post обязательными являются user_id, title, body
создайте связи relationship между моделями: User.posts и Post.user
"""

import os

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, relationship, sessionmaker

PG_CONN_URI = os.environ.get(
    "SQLALCHEMY_PG_CONN_URI") or "postgresql+asyncpg://postgres:password@localhost/postgres"

# DB_ECHO = True
DB_ECHO = False

engine = create_async_engine(
    url=PG_CONN_URI,
    echo=DB_ECHO,
)

Session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


class Base:

    @declared_attr
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=Base)


class User(Base):
    name = Column(
        String(32),
        nullable=False,
        unique=False,
    )
    username = Column(
        String(50),
        nullable=False,
        unique=True,
    )
    email = Column(
        String(100),
        nullable=True,
        unique=True,
    )

    posts = relationship(
        "Post",
        back_populates="user",
        uselist=True,
    )

    def __str__(self):
        return f"User: id={self.id}, name={self.name!r}, username={self.username!r}, email={self.email!r}"

    def __repr__(self):
        return str(self)


class Post(Base):
    title = Column(String(120), nullable=False, unique=False)
    body = Column(
        Text,
        nullable=False,
        unique=False,
        default="",
        server_default="",
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
    )

    user = relationship(
        "User",
        back_populates="posts",
        uselist=False,
    )

    def __str__(self):
        return f"Post: id={self.id}, title={self.title!r}, body={self.body!r}"

    def __repr__(self):
        return str(self)
