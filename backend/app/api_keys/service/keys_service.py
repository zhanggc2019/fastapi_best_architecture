#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import Select

from backend.app.api_keys.crud.crud_keys import api_keys_dao
from backend.app.api_keys.schema.keys import CreateApiKeysSchema
from backend.database.db import async_db_session


class ApiKeysService:

    @staticmethod
    async def get_list(*, name: str | None, user_id: str | None) -> Select:
        """
        获取结果列表查询条件

        :param name: 任务名称
        :param user_id: 任务 ID
        :return:
        """
        return await api_keys_dao.get_list(name, user_id)

    @staticmethod
    async def delete(*, pk: int, user_id: str) -> int:

        """
        删除apikey

        :param pk: api key主键
        :return:
        """
        async with async_db_session.begin() as db:
            count = await api_keys_dao.delete(db, pk, user_id)
            return count

    @staticmethod
    async def add_key(key_create: CreateApiKeysSchema):
        """
        生成key
        :return:
        """
        async with async_db_session.begin() as db:
            akd = await api_keys_dao.add(db, key_create=key_create)
            return akd


api_keys_service: ApiKeysService = ApiKeysService()
