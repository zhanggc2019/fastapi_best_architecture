#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.api_keys.api.v1.keys import router
from backend.core.conf import settings

v1 = APIRouter(prefix=f'{settings.FASTAPI_API_V1_PATH}/api_keys', tags=['api_keys管理'])

v1.include_router(router, prefix='/api_keys')
