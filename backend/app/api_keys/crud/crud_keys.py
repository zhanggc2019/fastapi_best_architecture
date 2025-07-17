#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.api_keys.model.keys import ApiKeys


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

        return await self.select_order('create_time', **filters)

    async def delete(self, db: AsyncSession, pks: list[int]) -> int:
        """
        批量删除任务结果

        :param db: 数据库会话
        :param pks: 任务结果 ID 列表
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pks)


api_keys_dao: ApiKeys = CRUDApiKeysResult(ApiKeys)
