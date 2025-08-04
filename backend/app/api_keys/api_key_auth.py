
from fastapi import Request

from backend.core.conf import settings
from backend.database.redis import redis_client


class ApiKeyAuth:
    """API Key认证类"""

    @staticmethod
    def get_api_key_from_request(request: Request) -> str | None:
        """从请求中提取API Key"""
        # 优先从Header中获取
        api_key = request.headers.get("X-API-Key") or request.headers.get("Authorization")

        if api_key and api_key.lower().startswith("bearer "):
            api_key = api_key[7:]  # 移除 "Bearer " 前缀

        # 如果Header中没有，从查询参数中获取
        if not api_key:
            api_key = request.query_params.get("api_key")
        return api_key

    @staticmethod
    async def authenticate_api_key(api_key: str | None) -> bool:
        """验证API Key并返回用户信息"""
        # 验证API Key
        api_key_str = await redis_client.get(f"{settings.API_KEY_REDIS_PREFIX}" + api_key)
        if not api_key_str:
            return False
        return True
        
    @staticmethod   
    async def get_current_user_by_api_key(request: Request) -> bool:
        """通过API Key获取当前用户"""
        api_key = ApiKeyAuth.get_api_key_from_request(request)
        if not api_key:
            return False
        return await ApiKeyAuth.authenticate_api_key(api_key)
