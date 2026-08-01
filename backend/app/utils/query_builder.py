from typing import Any
from sqlalchemy.sql.selectable import Select
from app.utils.pagination import PaginationParams

def apply_pagination_and_sort(
    query: Select,
    params: PaginationParams,
    model: Any,
    search_fields: list[str] | None = None
) -> Select:
    """
    Applies pagination, sorting, and optional searching to a SQLAlchemy query.
    """
    # 1. Search
    if params.search and search_fields:
        search_conditions = []
        for field in search_fields:
            column = getattr(model, field, None)
            if column is not None:
                search_conditions.append(column.ilike(f"%{params.search}%"))
        
        if search_conditions:
            from sqlalchemy import or_
            query = query.filter(or_(*search_conditions))

    # 2. Sort
    if params.sort_by:
        sort_column = getattr(model, params.sort_by, None)
        if sort_column is not None:
            if params.order.lower() == "desc":
                query = query.order_by(sort_column.desc())
            else:
                query = query.order_by(sort_column.asc())

    # 3. Pagination
    query = query.offset(params.skip).limit(params.limit)
    
    return query
