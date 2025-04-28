class Config:
    JWT_SECRET = "Come to the dark side, we have cookies"
    JWT_ALGORITHM = 'HS256'

    ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]