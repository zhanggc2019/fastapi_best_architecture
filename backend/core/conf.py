#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from functools import lru_cache
from typing import Any, Literal

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from backend.core.path_conf import BASE_PATH


class Settings(BaseSettings):
    """全局配置"""

    model_config = SettingsConfigDict(
        env_file=f'{BASE_PATH}/.env',
        env_file_encoding='utf-8',
        extra='ignore',
        case_sensitive=True,
    )

    # .env 环境
    ENVIRONMENT: Literal['dev', 'pro']

    # .env 数据库
    DATABASE_TYPE: Literal['mysql', 'postgresql']
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_USER: str
    DATABASE_PASSWORD: str

    # .env Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_DATABASE: int

    # .env Token
    TOKEN_SECRET_KEY: str  # 密钥 secrets.token_urlsafe(32)

    # .env 操作日志加密密钥
    OPERA_LOG_ENCRYPT_SECRET_KEY: str  # 密钥 os.urandom(32), 需使用 bytes.hex() 方法转换为 str

    # FastAPI
    FASTAPI_API_V1_PATH: str = '/api/v1'
    FASTAPI_TITLE: str = 'FastAPI'
    FASTAPI_VERSION: str = '1.5.0'
    FASTAPI_DESCRIPTION: str = 'FastAPI Best Architecture'
    FASTAPI_DOCS_URL: str = '/docs'
    FASTAPI_REDOC_URL: str = '/redoc'
    FASTAPI_OPENAPI_URL: str | None = '/openapi'
    FASTAPI_STATIC_FILES: bool = True

    # 数据库
    DATABASE_ECHO: bool | Literal['debug'] = False
    DATABASE_POOL_ECHO: bool | Literal['debug'] = False
    DATABASE_SCHEMA: str = 'fba'
    DATABASE_CHARSET: str = 'utf8mb4'

    # Redis
    REDIS_TIMEOUT: int = 5

    # Token
    TOKEN_ALGORITHM: str = 'HS256'
    TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7  # 7 天
    TOKEN_REFRESH_EXPIRE_SECONDS: int = 60 * 60 * 24 * 30  # 30 天
    TOKEN_REDIS_PREFIX: str = 'fba:token'
    TOKEN_EXTRA_INFO_REDIS_PREFIX: str = 'fba:token_extra_info'
    TOKEN_ONLINE_REDIS_PREFIX: str = 'fba:token_online'
    TOKEN_REFRESH_REDIS_PREFIX: str = 'fba:refresh_token'
    TOKEN_REQUEST_PATH_EXCLUDE: list[str] = [  # JWT / RBAC 路由白名单
        f'{FASTAPI_API_V1_PATH}/auth/login',
        f'{FASTAPI_API_V1_PATH}/auth/logout',
        '/apis/*',  # 开放 API 路由白名单, 开放api使用申请的key访问
    ]

    # JWT
    JWT_USER_REDIS_PREFIX: str = 'fba:user'

    # RBAC
    RBAC_ROLE_MENU_MODE: bool = True
    RBAC_ROLE_MENU_EXCLUDE: list[str] = [
        'sys:monitor:redis',
        'sys:monitor:server',
    ]

    # Cookie
    COOKIE_REFRESH_TOKEN_KEY: str = 'fba_refresh_token'
    COOKIE_REFRESH_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7  # 7 天

    # 数据权限配置
    DATA_PERMISSION_MODELS: dict[str, str] = {  # 允许进行数据过滤的 SQLA 模型，它必须以模块字符串的方式定义
        '部门': 'backend.app.admin.model.Dept',
    }
    DATA_PERMISSION_COLUMN_EXCLUDE: list[str] = [  # 排除允许进行数据过滤的 SQLA 模型列
        'id',
        'sort',
        'del_flag',
        'created_time',
        'updated_time',
    ]

    # Socket.IO
    WS_NO_AUTH_MARKER: str = 'internal'

    # CORS
    CORS_ALLOWED_ORIGINS: list[str] = [  # 末尾不带斜杠
        'http://127.0.0.1:8000',
        'http://localhost:5173',
    ]
    CORS_EXPOSE_HEADERS: list[str] = [
        'X-Request-ID',
    ]

    # 中间件配置
    MIDDLEWARE_CORS: bool = True

    # 请求限制配置
    REQUEST_LIMITER_REDIS_PREFIX: str = 'fba:limiter'

    # 时间配置
    DATETIME_TIMEZONE: str = 'Asia/Shanghai'
    DATETIME_FORMAT: str = '%Y-%m-%d %H:%M:%S'

    # 文件上传
    UPLOAD_READ_SIZE: int = 1024
    UPLOAD_IMAGE_EXT_INCLUDE: list[str] = ['jpg', 'jpeg', 'png', 'gif', 'webp']
    UPLOAD_IMAGE_SIZE_MAX: int = 5 * 1024 * 1024  # 5 MB
    UPLOAD_VIDEO_EXT_INCLUDE: list[str] = ['mp4', 'mov', 'avi', 'flv']
    UPLOAD_VIDEO_SIZE_MAX: int = 20 * 1024 * 1024  # 20 MB

    # 演示模式配置
    DEMO_MODE: bool = False
    DEMO_MODE_EXCLUDE: set[tuple[str, str]] = {
        ('POST', f'{FASTAPI_API_V1_PATH}/auth/login'),
        ('POST', f'{FASTAPI_API_V1_PATH}/auth/logout'),
        ('GET', f'{FASTAPI_API_V1_PATH}/auth/captcha'),
    }

    # IP 定位配置
    IP_LOCATION_PARSE: Literal['online', 'offline', 'false'] = 'offline'
    IP_LOCATION_REDIS_PREFIX: str = 'fba:ip:location'
    IP_LOCATION_EXPIRE_SECONDS: int = 60 * 60 * 24  # 1 天

    # 日志（Trace ID)
    TRACE_ID_REQUEST_HEADER_KEY: str = 'X-Request-ID'
    TRACE_ID_LOG_DEFAULT_VALUE: str = '-'
    TRACE_ID_LOG_UUID_LENGTH: int = 32  # UUID 长度，必须小于等于 32

    # 日志（控制台）
    LOG_STD_LEVEL: str = 'INFO'
    LOG_STD_FORMAT: str = (
        '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</> | <lvl>{level: <8}</> | <cyan>{correlation_id}</> | <lvl>{message}</>'
    )
    # 日志（文件）
    LOG_ACCESS_FILE_LEVEL: str = 'INFO'
    LOG_ERROR_FILE_LEVEL: str = 'ERROR'
    LOG_ACCESS_FILENAME: str = 'fba_access.log'
    LOG_ERROR_FILENAME: str = 'fba_error.log'
    LOG_FILE_FORMAT: str = '{time:YYYY-MM-DD HH:mm:ss.SSS} | <lvl>{level: <8}</> | {correlation_id} | <lvl>{message}</>'

    # 操作日志
    OPERA_LOG_PATH_EXCLUDE: list[str] = [
        '/favicon.ico',
        '/docs',
        '/redoc',
        '/openapi',
        f'{FASTAPI_API_V1_PATH}/auth/login/swagger',
        f'{FASTAPI_API_V1_PATH}/oauth2/github/callback',
        f'{FASTAPI_API_V1_PATH}/oauth2/linux-do/callback',
    ]
    OPERA_LOG_ENCRYPT_TYPE: int = 1  # 0: AES (性能损耗); 1: md5; 2: ItsDangerous; 3: 不加密, others: 替换为 ******
    OPERA_LOG_ENCRYPT_KEY_INCLUDE: list[str] = [  # 将加密接口入参参数对应的值
        'password',
        'old_password',
        'new_password',
        'confirm_password',
    ]

    # Plugin 配置
    PLUGIN_PIP_CHINA: bool = True
    PLUGIN_PIP_INDEX_URL: str = 'https://mirrors.aliyun.com/pypi/simple/'
    PLUGIN_REDIS_PREFIX: str = 'fba:plugin'

    # App Admin
    # .env OAuth2
    OAUTH2_GITHUB_CLIENT_ID: str
    OAUTH2_GITHUB_CLIENT_SECRET: str
    OAUTH2_LINUX_DO_CLIENT_ID: str
    OAUTH2_LINUX_DO_CLIENT_SECRET: str

    # OAuth2
    OAUTH2_FRONTEND_REDIRECT_URI: str = 'http://localhost:5173/oauth2/callback'

    # 验证码
    CAPTCHA_LOGIN_REDIS_PREFIX: str = 'fba:login:captcha'
    CAPTCHA_LOGIN_EXPIRE_SECONDS: int = 60 * 5  # 3 分钟

    # App Task
    # .env Redis
    CELERY_BROKER_REDIS_DATABASE: int

    # .env RabbitMQ
    # docker run -d --hostname fba-mq --name fba-mq  -p 5672:5672 -p 15672:15672 rabbitmq:latest
    CELERY_RABBITMQ_HOST: str
    CELERY_RABBITMQ_PORT: int
    CELERY_RABBITMQ_USERNAME: str
    CELERY_RABBITMQ_PASSWORD: str

    # 基础配置
    CELERY_BROKER: Literal['rabbitmq', 'redis'] = 'redis'
    CELERY_REDIS_PREFIX: str = 'fba:celery'
    CELERY_TASK_MAX_RETRIES: int = 5

    # API key 配置
    API_KEY_REDIS_PREFIX: str = 'fba:api_key:'

    # Plugin Code Generator
    CODE_GENERATOR_DOWNLOAD_ZIP_FILENAME: str = 'fba_generator'

    @model_validator(mode='before')
    @classmethod
    def check_env(cls, values: Any) -> Any:
        """检查环境变量"""
        if values.get('ENVIRONMENT') == 'pro':
            # FastAPI
            values['FASTAPI_OPENAPI_URL'] = None
            values['FASTAPI_STATIC_FILES'] = False
            # Task
            values['CELERY_BROKER'] = 'redis'  # 生产推荐rabbitmq

        return values


@lru_cache
def get_settings() -> Settings:
    """获取全局配置单例"""
    return Settings()


# 创建全局配置实例
settings = get_settings()
