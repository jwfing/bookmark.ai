from datetime import datetime
from enum import Enum as PyEnum
from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    password: str
    email: str = Field(unique=True)
    first_name: str
    last_name: str
    phone_number: str
    created_at: Optional[str] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[str] = Field(default_factory=datetime.utcnow)

class Bookmark(SQLModel, table=True):
    __tablename__ = "bookmarks"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    url: str
    url_md5: str
    created_at: Optional[str] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[str] = Field(default_factory=datetime.utcnow)

class BookmarkStatus(str, PyEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"

class BookmarkContent(SQLModel, table=True):
    __tablename__ = "bookmark_contents"

    url_md5: str = Field(primary_key=True)
    url: str
    status: BookmarkStatus = Field(default=BookmarkStatus.PENDING)
    title: str
    description: str
    content: str
    created_at: Optional[str] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[str] = Field(default_factory=datetime.utcnow)
