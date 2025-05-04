from dotenv import load_dotenv
from fastapi import FastAPI
from models.repository import create_db_and_tables
import uvicorn
from config import Config
from fastapi.middleware.cors import CORSMiddleware
from routers.endpoints import router

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

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(router)

if __name__ == "__main__":
    create_db_and_tables()
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=9000,
        reload=True,
        log_level="info"
    )