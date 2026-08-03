from typing import Generic, List, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class PaginationParams(BaseModel):
    skip: int = 0
    limit: int = 500
    search: str | None = None
    sort_by: str | None = None
    sort_order: str = "desc"

    @property
    def order(self) -> str:
        return self.sort_order

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    
    @classmethod
    def create(cls, items: List[T], total: int, params: PaginationParams):
        total_pages = (total + params.page_size - 1) // params.page_size
        return cls(
            items=items,
            total=total,
            page=params.page,
            page_size=params.page_size,
            total_pages=total_pages
        )
