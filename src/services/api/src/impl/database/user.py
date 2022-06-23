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
    descriminator: int = SmallInteger()
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
