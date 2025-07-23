#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.openapi.api.v1.apis import router

v1 = APIRouter(prefix='/apis', tags=['开放API'])
v1.include_router(router, prefix='')

