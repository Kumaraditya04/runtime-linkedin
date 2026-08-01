from fastapi import APIRouter
from app.core.responses import StandardResponse, success_response

router = APIRouter()

@router.get("/health", response_model=StandardResponse[dict])
async def health_check():
    return success_response(
        message="Service is healthy", 
        data={"status": "ok"}
    )

@router.get("/version", response_model=StandardResponse[dict])
async def get_version():
    return success_response(
        message="Version information", 
        data={"version": "1.0.0"}
    )

@router.get("/ping", response_model=StandardResponse[dict])
async def ping():
    return success_response(
        message="Pong", 
        data={"ping": "pong"}
    )
