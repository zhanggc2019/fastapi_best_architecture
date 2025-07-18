import base64
import hmac
import secrets

from datetime import datetime
from typing import Optional

from backend.core.conf import settings

SECRET_KEY = settings.TOKEN_SECRET_KEY.encode()  # 必须保密！


def generate_signed_api_key(user_id: str, expires_in_days: Optional[int] = 0):
    """
    生成签名后的 API Key
    :param user_id: 用户 ID
    :param expires_in_days: 过期时间（天）
    :return: 签名后的 API Key
    """
    k = secrets.token_urlsafe(32)
    # todo 明文保存，后期优化
    # if expires_in_days:
    #     expires_at = int((datetime.now() + timedelta(days=expires_in_days)).timestamp())
    #     data = f"{user_id}:{expires_at}:{k}".encode()
    # else:
    #     data = f"{user_id}:-1:{k}".encode()
    # signature = hmac.new(SECRET_KEY, data, digestmod="sha256").digest()

    return 'sk-' + k


def verify_signed_api_key(api_key: str):
    api_key = api_key[3:]  # 去除sk开头检验
    try:
        decoded = base64.urlsafe_b64decode(api_key.encode())
        data, signature = decoded.split(b".", 1)
        user_id, _, expires_at = data.decode().split(":")

        # 验证签名
        expected_signature = hmac.new(SECRET_KEY, data, digestmod="sha256").digest()
        if not hmac.compare_digest(signature, expected_signature):
            return user_id, False
        if expires_at == "-1":
            return user_id, True
        # 验证时间
        return user_id, datetime.now().timestamp() < int(expires_at)
    except Exception:
        return user_id, False
