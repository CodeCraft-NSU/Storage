from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from dotenv import load_dotenv
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import os

from project import router as project_router
from upload import router as upload_router

app = FastAPI(debug=True)

load_dotenv()
API_KEY = os.getenv('API_KEY')

class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        authorization = request.headers.get("Authorization")
        if authorization != API_KEY:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return await call_next(request)

app.add_middleware(APIKeyMiddleware)

# 예외 핸들러
@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    print(f"Unhandled error: {str(exc)}")  # 콘솔에 전체 예외 출력
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred", "error": str(exc)},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"Validation error: {exc.errors()}")  # 콘솔에 검증 오류 출력
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

@app.get("/")
async def root():
    return {"message": "root of PMS Storage Server API."}

app.include_router(project_router, prefix="/api")
app.include_router(upload_router, prefix="/api")