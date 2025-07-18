#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Body, Query, Request

from backend.app.admin.model.user import User
from backend.app.api_keys.schema.keys import ApiKeysSchema, CreateApiKeysSchema, UserCreateApiKeysSchema
from backend.app.api_keys.service.keys_service import api_keys_service
from backend.app.api_keys.utils import generate_signed_api_key
from backend.common.pagination import DependsPagination, PageData, paging_data
from backend.common.response.response_code import CustomResponse
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth, jwt_decode, superuser_verify
from backend.database.db import CurrentSession

router = APIRouter()


@router.get('/list', summary='分页获取用户下所有api_keys', dependencies=[DependsPagination])
async def get_keys_paged(
    db: CurrentSession,
    request: Request,
    user: User = DependsJwtAuth,  # 从认证依赖获取用户对象
    name: Annotated[str | None, Query(description='key名称')] = None,
) -> ResponseSchemaModel[PageData[ApiKeysSchema]]:
    auth_user = jwt_decode(user.credentials)
    is_superuser = superuser_verify(request)
    if is_superuser:
        user_id = None
    else:
        user_id = auth_user.id
    result_select = await api_keys_service.get_list(name=name, user_id=user_id)
    page_data = await paging_data(db, result_select)
    return response_base.success(data=page_data)


@router.delete('', summary='删除key')
async def delete_api_key(user: User = DependsJwtAuth, id: int = Body(embed=True)) -> ResponseModel:
    auth_user = jwt_decode(user.credentials)
    count = await api_keys_service.delete(pk=id, user_id=auth_user.id)
    if count > 0:
        return response_base.success()
    res = CustomResponse(code=400, msg='key不存在')
    return response_base.fail(res=res)


@router.post('/add', summary='新增key')
async def add_api_key(key: UserCreateApiKeysSchema, user: User = DependsJwtAuth) -> ResponseModel:
    auth_user = jwt_decode(user.credentials)
    api_key = generate_signed_api_key(user_id=str(auth_user.id), expires_in_days=key.expire_time)
    key_create = CreateApiKeysSchema(
        user_id=str(auth_user.id),
        api_key=api_key,
        name=key.name,
        expire_time=key.expire_time,
    )
    api_key = await api_keys_service.add_key(key_create=key_create)
    if api_key:
        return response_base.success()
    return response_base.fail()
