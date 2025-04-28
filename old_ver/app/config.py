import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # 应用配置
    APP_ENV = os.getenv('APP_ENV', 'development')
    DEBUG = os.getenv('DEBUG', 'true').lower() == 'true'

    # PostgreSQL 配置
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'bookmarkuser')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'password')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'bookmarkdb')

    # OpenAI 配置
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    # LlamaIndex 配置
    CHUNK_SIZE = 800
    CHUNK_OVERLAP = 50

    @classmethod
    def get_database_url(cls):
        return f"postgresql://{cls.POSTGRES_USER}:{cls.POSTGRES_PASSWORD}@{cls.POSTGRES_HOST}:{cls.POSTGRES_PORT}/{cls.POSTGRES_DB}"

    # 模型配置
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'qwen')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY')

    @classmethod
    def validate(cls):
        """验证必需的配置项"""
        if cls.EMBEDDING_MODEL == 'openai' and not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required when using OpenAI model")
        elif cls.EMBEDDING_MODEL == 'qwen' and not cls.DASHSCOPE_API_KEY:
            raise ValueError("DASHSCOPE_API_KEY is required when using Qwen model")