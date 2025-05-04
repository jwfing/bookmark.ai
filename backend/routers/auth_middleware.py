from functools import wraps
from fastapi import HTTPException, Request
from typing import Callable
from utils.jwt_helper import decode_jwt_token

def require_auth(func: Callable):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        request = args[0]
        authorization = request.headers.get('Authorization')
        if not authorization:
            raise HTTPException(status_code=401, detail="Unauthorized")
        try:
            token = authorization.split(" ")[1]
            payload = decode_jwt_token(token)
            user_id = payload.get("user_id")
            if user_id is None:
                raise HTTPException(status_code=401, detail="Unauthorized")
            # 将 user_id 添加到 kwargs
            kwargs["user_id"] = user_id
            return await func(request, *args, **kwargs)
        except Exception as e:
            raise HTTPException(status_code=401, detail="Unauthorized")
    return wrapper