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


class ApiKeys(Base):
    """api keys管理表"""

    __tablename__ = 'api_keys'
    id: Mapped[id_key] = mapped_column(init=False, comment='主键')
    api_key: Mapped[str] = mapped_column(String(100), unique=True, comment='api_key_hash')
    name: Mapped[str] = mapped_column(String(50), comment='api key名称')
    user_id: Mapped[str] = mapped_column(String(255), comment='key所属用户id')
    expire_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None, comment='key过期截止时间'
    )
    enabled: Mapped[bool] = mapped_column(
        Boolean().with_variant(INTEGER, 'postgresql'), default=True, comment='是否启用key'
    )
    scope: Mapped[str | None] = mapped_column(String(255), default=None, comment='权限范围,如read,write 默认None所有')
