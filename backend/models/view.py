from typing import Optional
from pydantic import BaseModel, model_validator

class UserAuth(BaseModel):
    id: str
    username: str
    email: str

class SearchQuery(BaseModel):
    query: str

class LoginForm(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: str

    @model_validator(mode='after')  # 使用 'after' 模式确保字段已基本验证
    def check_username_or_email(self) -> 'LoginForm':
        """Ensures that either username or email is provided."""
        if self.username is None and self.email is None:
            raise ValueError('Either username or email must be provided')
        return self

class Bookmark(BaseModel):
    id: str
    title: str
    url: str
    description: str
    user_id: str