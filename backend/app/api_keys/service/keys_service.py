#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import Select

from backend.app.api_keys.crud.crud_keys import api_keys_dao
from backend.app.api_keys.model.keys import ApiKeys
from backend.app.api_keys.schema.keys import DeleteApiKeysSchema
from backend.common.exception import errors
from backend.database.db import async_db_session


class ApiKeysService:
    @staticmethod
    async def get(*, pk: int) -> ApiKeys:
        """
        获取任务结果详情

        :param pk: 任务 ID
        :return:
        """
        async with async_db_session() as db:
            result = await api_keys_dao.get(db, pk)
            if not result:
                raise errors.NotFoundError(msg='任务结果不存在')
            return result

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
    async def delete(*, obj: DeleteApiKeysSchema) -> int:
        """
        批量删除任务结果

        :param obj: 任务结果 ID 列表
        :return:
        """
        async with async_db_session.begin() as db:
            count = await api_keys_dao.delete(db, obj.pks)
            return count

    @staticmethod
    async def add_key(user_id: str):
        """
        生成key

        :return:
        """
        import binascii
        import secrets
        import string

        alphabet = string.ascii_letters + string.digits
        random_str = ''.join(secrets.choice(alphabet) for _ in range(10))
        key_body = f"{user_id}_{random_str}"
        crc8 = binascii.crc32(key_body.encode()) & 0xFF
        checksum = f"{crc8:02x}" 
        api_key = f"sk-{key_body}_{checksum}"
        # 示例输出: "sk-mno_usr123_5xQ9kP2Lb8_7f"
        await api_key


api_keys_service: ApiKeysService = ApiKeysService()
