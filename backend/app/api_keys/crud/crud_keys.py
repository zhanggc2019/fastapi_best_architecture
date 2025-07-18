#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.api_keys.model.keys import ApiKeys
from backend.app.api_keys.schema.keys import CreateApiKeysSchema


class CRUDApiKeysResult(CRUDPlus[ApiKeys]):
    """结果数据库操作类"""

    async def get_list(self, name: str | None, user_id: str | None) -> Select:
        """
        获取任务结果列表

        :param name:名称
        :param user_id: 用户ID
        :return:
        """
        filters = {}

        if name is not None:
            filters['name__like'] = f'%{name}%'
        if user_id is not None:
            filters['user_id'] = user_id
        # self.select_models_order
        return await self.select_order(sort_columns=['created_time'], **filters)

    async def delete(self, db: AsyncSession, pk: int, user_id: str) -> int:
        """
        删除api key

        :param db: 数据库会话
        :param pk: api key主键
        :param user_id: api key所属用户id
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=False, id=pk, user_id=user_id)

    async def add(self, db: AsyncSession, key_create: CreateApiKeysSchema) -> int:
        """
        添加api key

        :param db: 数据库会话
        :param user_id: api key所属用户id
        :return:
        """
        obj = CreateApiKeysSchema(
            user_id=key_create.user_id,
            api_key=key_create.api_key,
            name=key_create.name,
            expire_time=key_create.expire_time,
        )
        return await self.create_model(db, obj=obj)


api_keys_dao: CRUDApiKeysResult = CRUDApiKeysResult(ApiKeys)
