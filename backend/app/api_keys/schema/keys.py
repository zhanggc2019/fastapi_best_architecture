#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import Field, field_validator

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
    expire_time: datetime | None = Field(description='过期时间,格式需要满足 "%Y-%m-%d %H:%M:%S"')

    @field_validator('expire_time', mode='before')
    def validate_expire_time_format(cls, value):
        if value is None:
            return value
        # 如果是datetime对象则直接返回
        if isinstance(value, datetime):
            return value
        # 验证字符串格式
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                raise ValueError("过期时间格式错误，请使用 '%Y-%m-%d %H:%M:%S' 格式")
        raise ValueError(f"过期时间必须是有效的日期时间字符串或datetime对象，当前类型: {type(value)}")

