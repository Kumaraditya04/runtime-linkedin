from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import Base
from app.repositories.base import BaseRepository

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, repository: BaseRepository[ModelType, CreateSchemaType, UpdateSchemaType]):
        self.repository = repository

    async def get(self, db: AsyncSession, id: Any) -> ModelType:
        obj = await self.repository.get(db, id)
        if not obj:
            raise HTTPException(status_code=404, detail="Resource not found")
        return obj

    async def get_multi(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return await self.repository.get_multi(db, skip=skip, limit=limit)
        
    async def count(self, db: AsyncSession) -> int:
        return await self.repository.count(db)

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        return await self.repository.create(db, obj_in=obj_in)

    async def update(self, db: AsyncSession, id: Any, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        db_obj = await self.get(db, id)
        return await self.repository.update(db, db_obj=db_obj, obj_in=obj_in)

    async def remove(self, db: AsyncSession, id: Any) -> ModelType:
        await self.get(db, id) # Ensure exists
        return await self.repository.remove(db, id=id)
