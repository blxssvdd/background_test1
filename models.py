import os
import asyncio
from typing import Optional

from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, relationship
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv


load_dotenv()
SQLALCHEMY_URI = os.getenv("SQLALCHEMY_URI")
engine = create_async_engine(SQLALCHEMY_URI, echo=True)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(100))


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    send_mail: Mapped[str] = mapped_column(Text())
    incoming: Mapped[Optional[str]] = mapped_column(Text(), nullable=True, default=None)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship()


async def create_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)


async def get_db():
    async with Session() as session:
        yield session


if __name__ == "__main__":
    asyncio.run(create_db())


