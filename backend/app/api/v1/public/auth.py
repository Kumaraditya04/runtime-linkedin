from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.deps import get_db
from app.config import settings
from app.core import security
from app.core.responses import StandardResponse, success_response, error_response
from app.models.admin import Admin
from app.schemas.auth import TokenResponse, AdminResponse

router = APIRouter()

@router.post("/login", response_model=StandardResponse[dict])
async def login_access_token(
    response: Response,
    session: AsyncSession = Depends(get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    result = await session.execute(select(Admin).where(Admin.email == form_data.username))
    admin = result.scalar_one_or_none()
    
    if not admin or not security.verify_password(form_data.password, admin.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not admin.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
        
    access_token = security.create_access_token(
        admin.id, role=admin.role
    )
    
    # Set HttpOnly Cookie (Cross-domain ready)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=True,
        samesite="none",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    
    return success_response(
        message="Login successful",
        data={"role": admin.role, "access_token": access_token, "token_type": "bearer"}
    )

@router.post("/logout", response_model=StandardResponse[dict])
async def logout(response: Response) -> Any:
    response.delete_cookie(key="access_token", path="/", httponly=True, samesite="none", secure=True)
    return success_response(message="Logged out successfully", data={})
