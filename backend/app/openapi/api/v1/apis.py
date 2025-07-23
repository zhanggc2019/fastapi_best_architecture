#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

from fastapi import APIRouter, Depends, HTTPException, Request

from backend.app.api_keys.service.keys_service import api_keys_service
from backend.common.response.response_schema import ResponseModel, response_base

router = APIRouter()


async def auth_api_key(request: Request) -> bool:
    is_auth = await api_keys_service.validate_api_key(request)
    if is_auth is False:
        raise HTTPException(status_code=400, detail='api key不合法或已过期')
    return is_auth


@router.get('/test', summary='一个受保护的API', dependencies=[Depends(auth_api_key)])
async def protected() -> ResponseModel:
    return response_base.success(data=f"Hello, World! {time.time()}")

