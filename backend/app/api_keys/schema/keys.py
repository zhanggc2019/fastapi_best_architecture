#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import Field

from backend.common.schema import SchemaBase


class ApiKeysSchema(SchemaBase):
    """基础模型"""

    id: int = Field(description='主键ID')
    api_key: str | None = Field(description='api_key_hash')
    name: str | None = Field(description='api_key名称')
    user_id: str = Field(description='key所属用户')
    expire_time: datetime | None = Field(description='过期时间')
    created_time: datetime = Field(description='创建时间')
    enabled: bool | None = Field(description='是否可用')
    scope: str | None = Field(description='权限范围,如read,write 默认None所有')


class CreateApiKeysSchema(SchemaBase):
    """新增模型"""

    api_key: str | None = Field(description='api_key_hash')
    name: str | None = Field(description='api_key名称')
    user_id: str = Field(description='key所属用户')
    expire_time: datetime | None = Field(description='过期时间')


class UserCreateApiKeysSchema(SchemaBase):
    """用户新增key"""
    name: str = Field(..., description='api_key名称')
    expire_time: datetime | None = Field(description='过期时间')

