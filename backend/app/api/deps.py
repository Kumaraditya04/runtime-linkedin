from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.config import settings
from app.database.database import get_db
from app.models.admin import Admin
from app.schemas.auth import TokenPayload

from fastapi import Request

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/public/auth/login",
    auto_error=False
)

SessionDep = Annotated[AsyncSession, Depends(get_db)]

async def get_token(request: Request, token: str = Depends(reusable_oauth2)) -> str:
    if not token:
        cookie_token = request.cookies.get("access_token")
        if cookie_token and cookie_token.startswith("Bearer "):
            return cookie_token.split(" ")[1]
        elif cookie_token:
            return cookie_token
    return token

TokenDep = Annotated[str, Depends(get_token)]

async def get_current_admin(session: SessionDep, token: TokenDep) -> Admin:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    
    if not token_data.sub:
        raise HTTPException(status_code=404, detail="Admin not found")
        
    result = await session.execute(select(Admin).where(Admin.id == int(token_data.sub)))
    admin = result.scalar_one_or_none()
    
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    if not admin.is_active:
        raise HTTPException(status_code=400, detail="Inactive admin")
    return admin

# RBAC Dependencies
def require_role(allowed_roles: list[str]):
    async def role_checker(current_admin: Admin = Depends(get_current_admin)):
        if current_admin.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted"
            )
        return current_admin
    return role_checker

# Helper for standard admin access
get_admin_role = require_role(["admin"])
