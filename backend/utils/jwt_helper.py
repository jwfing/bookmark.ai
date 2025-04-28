from datetime import datetime, timedelta
import jwt
from config import Config

def create_jwt_token(data: dict) -> str:
    if isinstance(data.get('user_id'), dict):
        user_id = data['user_id'].get('user_id')
    else:
        user_id = data.get('user_id')

    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(days=30)
    }

    return jwt.encode(
        payload,
        Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )

def decode_jwt_token(token: str) -> dict:
    return jwt.decode(
        token,
        Config.JWT_SECRET,
        algorithms=[Config.JWT_ALGORITHM]
    )