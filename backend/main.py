from dotenv import load_dotenv
from fastapi import FastAPI, Response, Depends, Header
from typing import Annotated
from models.view import LoginForm, SearchQuery, PageIndexing
from sqlmodel import Session
from models.repository import get_session, create_db_and_tables
import uvicorn
from utils.jwt_helper import create_jwt_token, decode_jwt_token
from config import Config
from fastapi.middleware.cors import CORSMiddleware
from rag.retriever import Retriever
from rag.data_source import vector_store
from rag.indexing import Indexing

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,
)

retriever = Retriever(vector_store)
indexing = Indexing(vector_store)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/signin")
async def signin(request: LoginForm, response: Response, db: Session = Depends(get_session)):
    token = create_jwt_token({"user_id": request.username or request.email})
    response.set_cookie(key="token", value=f"{token}", httponly=True, samesite="lax", secure=False, path="/")
    return {"result": "success", "token": token}

@app.post("/pages")
async def index_page(request: PageIndexing, response: Response, authorization: Annotated[str | None, Header()] = None,
                     db: Session = Depends(get_session)):
    if not authorization:
        response.status_code = 401
        return {"result": "error", "message": "Token is required"}
    decode_token = decode_jwt_token(authorization.split(' ')[1])
    if 'user_id' not in decode_token:
        response.status_code = 401
        return {"result": "error", "message": "Token is invalid"}
    user_id = decode_token['user_id']
    await indexing.index(request.url)
    return {"result": "success", "message": "Page indexed successfully"}

@app.post("/search")
async def search(search_request: SearchQuery, response: Response, authorization: Annotated[str | None, Header()] = None,
                 db: Session = Depends(get_session)):
    if not authorization:
        response.status_code = 401
        return {"result": "error", "message": "Token is required"}
    decode_token = decode_jwt_token(authorization.split(' ')[1])
    if 'user_id' not in decode_token:
        response.status_code = 401
        return {"result": "error", "message": "Token is invalid"}
    user_id = decode_token['user_id']
    rag_result = retriever.retrieve_and_generate(search_request.query)
    if rag_result:
        response.status_code = 200
    else:
        response.status_code = 404
    return {"result": "success", "message": rag_result['answer'], "query": search_request.query}

if __name__ == "__main__":
    create_db_and_tables()
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=9000,
        reload=True,
        log_level="info"
    )