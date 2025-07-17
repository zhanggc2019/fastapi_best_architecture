#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from backend.app.admin.model.user import User
from backend.app.api_keys.schema.keys import ApiKeysSchema, DeleteApiKeysSchema
from backend.app.api_keys.service.keys_service import api_keys_service
from backend.common.pagination import DependsPagination, PageData, paging_data
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth, superuser_verify
from backend.database.db import CurrentSession
from fastapi import APIRouter, Depends, Query, Request

router = APIRouter()


@router.get('', summary='分页获取用户下所有api_keys', dependencies=[DependsJwtAuth, DependsPagination])
async def get_keys_paged(
    db: CurrentSession,
    request: Request,
    user: User = Depends(DependsJwtAuth),  # 从认证依赖获取用户对象
    name: Annotated[str | None, Query(description='key名称')] = None,
) -> ResponseSchemaModel[PageData[ApiKeysSchema]]:
    print(user.id)
    is_superuser = superuser_verify(request)
    print(is_superuser)
    result_select = await api_keys_service.get_list(name=name, user_id=user.id)
    page_data = await paging_data(db, result_select)
    return response_base.success(data=page_data)


@router.delete(
    '',
    summary='删除key',
)
async def delete_api_key(obj: DeleteApiKeysSchema) -> ResponseModel:
    count = await api_keys_service.delete(obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.post(
    '',
    summary='新增key',
)
async def add_api_key() -> ResponseModel:
    # user_id
    user_id = ''
    count = await api_keys_service.add_key(user_id=user_id)
    if count > 0:
        return response_base.success()
    return response_base.fail()
