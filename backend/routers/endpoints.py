from fastapi import APIRouter, Response, Depends, UploadFile
from models.view import LoginForm, SearchQuery, PageIndexing
from sqlmodel import Session
from utils.jwt_helper import create_jwt_token
from models.repository import get_session
from rag.retriever import Retriever
from rag.data_source import vector_store
from rag.indexing import Indexing
from routers.auth_middleware import require_auth

router = APIRouter()
retriever = Retriever(vector_store)
indexing = Indexing(vector_store)

@router.post("/signin")
async def signin(request: LoginForm, response: Response, db: Session = Depends(get_session)):
    token = create_jwt_token({"user_id": request.username or request.email})
    response.set_cookie(key="token", value=f"{token}", httponly=True, samesite="lax", secure=False, path="/")
    return {"result": "success", "token": token}

@router.post("/signup")
async def signup(request: LoginForm, response: Response, db: Session = Depends(get_session)):
    token = create_jwt_token({"user_id": request.username or request.email})
    response.set_cookie(key="token", value=f"{token}", httponly=True, samesite="lax", secure=False, path="/")
    return {"result": "success", "token": token}

@router.post("/pages")
async def index_page(request: PageIndexing, user_id: str, response: Response,
                     db: Session = Depends(get_session)):
    await indexing.index(request.url)
    return {"result": "success", "message": "Page indexed successfully"}

@router.post("/import")
async def import_pages(bookmark_file: UploadFile, user_id: str, response: Response,
                       db: Session = Depends(get_session)):
    return {"result": "success", "message": "Page indexed successfully"}

@router.post("/search")
@require_auth
async def search(search_request: SearchQuery, user_id: str, response: Response,
                 db: Session = Depends(get_session)):
    rag_result = retriever.retrieve_and_generate(search_request.query)
    if rag_result:
        response.status_code = 200
    else:
        response.status_code = 404
    return {"result": "success", "message": rag_result['answer'], "query": search_request.query}
