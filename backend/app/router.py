#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.admin.api.router import v1 as admin_v1
from backend.app.api_keys.api.router import v1 as api_keys_v1
from backend.app.openapi.api.router import v1 as openapi_v1
from backend.app.task.api.router import v1 as task_v1

router = APIRouter()

router.include_router(admin_v1)
router.include_router(task_v1)
router.include_router(api_keys_v1)
router.include_router(openapi_v1)
