from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import ARRAY, FLOAT
from pgvector.sqlalchemy import Vector
from datetime import datetime
from app.config import Config

Base = declarative_base()

class RawPage(Base):
    __tablename__ = 'raw_pages'
    
    id = Column(Integer, primary_key=True)
    owner = Column(String(255))
    url = Column(String(2048), unique=True)
    content = Column(Text)
    raw_content = Column(Text)
    status = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class PageVectorIndex(Base):
    __tablename__ = 'page_vector_index'
    
    id = Column(Integer, primary_key=True)
    page_id = Column(Integer)
    chunk_index = Column(Integer)
    chunk_text = Column(Text)
    embedding = Column(Vector(1536))  # 使用 pgvector 的 Vector 类型
    meta_info = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

# 数据库连接配置
engine = create_engine(Config.get_database_url())
SessionLocal = sessionmaker(bind=engine)

def init_db():
    # 验证配置
    Config.validate()
    
    # 创建 pgvector 扩展
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()
        
    Base.metadata.create_all(engine)
    
    # 创建向量索引，使用 cosine 距离
    with engine.connect() as conn:
        conn.execute(text("""
        CREATE INDEX IF NOT EXISTS embedding_idx 
        ON page_vector_index 
        USING ivfflat (embedding vector_ip_ops)
        WITH (lists = 100)
        """))
        conn.commit()

init_db()