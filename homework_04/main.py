"""
Домашнее задание №4
Асинхронная работа с сетью и бд

доработайте функцию main, по вызову которой будет выполняться полный цикл программы
(добавьте туда выполнение асинхронной функции async_main):
- создание таблиц (инициализация)
- загрузка пользователей и постов
    - загрузка пользователей и постов должна выполняться конкурентно (параллельно)
      при помощи asyncio.gather (https://docs.python.org/3/library/asyncio-task.html#running-tasks-concurrently)
- добавление пользователей и постов в базу данных
  (используйте полученные из запроса данные, передайте их в функцию для добавления в БД)
- закрытие соединения с БД
"""
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from jsonplaceholder_requests import fetch_users_data, fetch_posts_data
from models import (
    User,
    Post,
    engine,
    Session,
    Base,
)


async def create_user(session: AsyncSession, name: str, username: str, email: str = None) -> User:
    user = User(name=name, username=username, email=email)
    session.add(user)
    await session.commit()
    return user


async def create_users(session: AsyncSession, users_data: list) -> None:
    users = [
        User(
            id=el['id'],
            name=el['name'],
            username=el['username'],
            email=el['email'],
        )
        for el in users_data
    ]
    session.add_all(users)
    await session.commit()


async def create_post(session: AsyncSession, title: str, user_id: int, body: str = "") -> None:
    post = Post(title=title, body=body, user_id=user_id)
    session.add(post)
    await session.commit()


async def create_posts(session: AsyncSession, posts_data: list) -> None:
    posts = [
        Post(
            id=el['id'],
            title=el['title'],
            body=el['body'],
            user_id=el['userId'],
        )
        for el in posts_data
    ]
    session.add_all(posts)
    await session.commit()



async def set_dates():
    async with Session() as session:
        users_data: list[User]
        posts_data: list[Post]
        users_data, posts_data = await asyncio.gather(
            fetch_users_data(),
            fetch_posts_data(),
        )
        await create_users(session=session, users_data=users_data)
        await create_posts(session=session, posts_data=posts_data)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


async def async_main():
    await drop_tables()
    await create_tables()
    await set_dates()


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
