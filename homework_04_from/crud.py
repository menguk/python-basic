import asyncio

from sqlalchemy import delete, select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from models import User, Post


async def create_user(session: AsyncSession, name: str, username: str, email: str = None) -> None:
    user = User(name=name, username=username, email=email)
    session.add(user)
    await session.commit()


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


async def get_users(session: AsyncSession) -> list[User]:
    stmt = (
        select(User)
        .order_by(User.id)
    )
    result: Result = await session.execute(stmt)
    users: list[User] = result.scalars().all()
    print(users)
    return users


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


async def delete_user(session: AsyncSession, user_id: int) -> None:
    stmt = (
        delete(User)
        .where(User.id == user_id)

    )
    await session.execute(stmt)
    await session.commit()


async def clear_table_users(session: AsyncSession) -> None:
    stmt = (
        delete(User)
    )
    await session.execute(stmt)
    await session.commit()


async def delete_post(session: AsyncSession, post_id: int) -> None:
    stmt = (
        delete(Post)
        .where(Post.id == post_id)

    )
    await session.execute(stmt)
    await session.commit()


async def clear_table_posts(session: AsyncSession) -> None:
    stmt = (
        delete(Post)
    )
    await session.execute(stmt)
    await session.commit()
