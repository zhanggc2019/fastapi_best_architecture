#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from sqlalchemy import (
    Boolean,
    DateTime,
    String,
)
from sqlalchemy.dialects.postgresql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key
from backend.core.conf import settings
from backend.database.redis import redis_client
from backend.utils.timezone import timezone


class ApiKeys(Base):
    """api keys管理表"""

    __tablename__ = 'api_keys'
    id: Mapped[id_key] = mapped_column(init=False, comment='主键')
    api_key: Mapped[str] = mapped_column(String(50), comment='api_key_hash')
    name: Mapped[str] = mapped_column(String(50), unique=True, comment='api key名称')
    user_id: Mapped[str] = mapped_column(String(255), comment='key所属用户id')
    expire_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now() + timedelta(days=30), comment='key过期截止时间'
    )
    create_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=datetime.now, comment='key创建时间'
    )
    enabled: Mapped[bool] = mapped_column(
        Boolean().with_variant(INTEGER, 'postgresql'), default=True, comment='是否启用key'
    )
    scope: Mapped[str | None] = mapped_column(String(255), default=None, comment='权限范围,如read,write 默认None所有')

    @classmethod
    def changed(cls, mapper, connection, target):
        if not target.no_changes:
            cls.update_changed(mapper, connection, target)

    @classmethod
    async def update_changed_async(cls):
        now = timezone.now()
        await redis_client.set(f'{settings.API_KEY_REDIS_PREFIX}:last_update', timezone.to_str(now))
