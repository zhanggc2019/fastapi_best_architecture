#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import Field

from backend.common.schema import SchemaBase


class ApiKeysSchema(SchemaBase):
    """基础模型"""

    id: str = Field(description='主键ID')
    api_key: str | None = Field(description='api_key_hash')
    name: str | None = Field(description='api_key名称')
    user_id: str = Field(description='key所属用户')
    expire_time: datetime | None = Field(description='过期时间')
    create_time: datetime = Field(description='创建时间')
    enabled: bool | None = Field(description='是否可用')
    scope: str | None = Field(description='权限范围,如read,write 默认None所有')


class DeleteApiKeysSchema(ApiKeysSchema):
    """删除模型"""

    id: str = Field(description='主键ID')

