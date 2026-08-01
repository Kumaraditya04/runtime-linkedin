from typing import Generic, List, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 20
    search: str | None = None
    sort_by: str | None = None
    order: str = "asc" # asc or desc

    @property
    def skip(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size

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
