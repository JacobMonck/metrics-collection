from datetime import datetime
from typing import Optional

from ormar import BigInteger, Boolean, DateTime, Model, SmallInteger, String

from .database import database, metadata


class User(Model):
    class Meta:
        database = database
        metadata = metadata
        tablename = "users"

    id: int = BigInteger(primary_key=True)
    username: str = String(max_length=32)
    nickname: str = String(max_length=32)
    discriminator: int = SmallInteger()
    joined_at: datetime = DateTime()
    created_at: datetime = DateTime()
    premium_since: Optional[datetime] = DateTime(nullable=True)
    in_guild: bool = Boolean()
    pending: bool = Boolean()
    staff: bool = Boolean()
    bot: bool = Boolean()
    online: bool = Boolean()
    raw_status: str = String(max_length=20)
    on_mobile: bool = Boolean()

    @staticmethod
    async def bulk_upsert(users: list["User"]) -> None:
        users = [
            [
                user.id,
                user.username,
                user.nickname,
                user.discriminator,
                user.joined_at,
                user.created_at,
                user.premium_since,
                user.in_guild,
                user.pending,
                user.staff,
                user.bot,
                user.online,
                user.raw_status,
                user.on_mobile,
            ]
            for user in users
        ]

        await database.execute_many(
            """
            INSERT INTO users (
                id, 
                username, 
                nickname, 
                discriminator, 
                joined_at, 
                created_at,
                premium_since, 
                in_guild, 
                pending, 
                staff, 
                bot, 
                online, 
                raw_status, 
                on_mobile
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
            ON CONFLICT (id)
            DO UPDATE SET
                username = EXCLUDED.username,
                nickname = EXCLUDED.nickname,        
                discriminator = EXCLUDED.discriminator,
                joined_at = EXCLUDED.joined_at, 
                created_at = EXCLUDED.created_at, 
                premium_since = EXCLUDED.premium_since, 
                in_guild = EXCLUDED.in_guild, 
                pending = EXCLUDED.pending, 
                staff = EXCLUDED.staff, 
                bot = EXCLUDED.bot, 
                raw_status = EXCLUDED.raw_status,
                on_mobile = EXCLUDED.on_mobile;
            """,
            users,
        )
