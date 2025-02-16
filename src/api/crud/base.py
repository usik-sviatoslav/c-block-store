from typing import Any, Generic, TypeVar
from uuid import UUID

from django.db import models
from django.db.models import QuerySet
from pydantic import BaseModel

__all__ = ["CRUDBase"]


ModelType = TypeVar("ModelType", bound=models.Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType]):
        """Initialize the CRUDBase instance with a Django model and a Pydantic schema."""
        self.model = model

    def get_queryset(self, **kwargs: Any) -> QuerySet[ModelType]:
        return self.model.objects.filter(**kwargs)  # type: ignore

    async def get(self, pk: int | UUID) -> ModelType | None:
        """Retrieve a Django model instance by ID."""
        return await self.get_queryset(id=pk).afirst()

    async def get_list(self, skip: int = 0, limit: int = 100, **kwargs: Any) -> list[ModelType | None]:
        """Retrieve a list of Django model instances from the database, with optional pagination."""
        start, end = skip * limit, skip * limit + limit
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        queryset = self.get_queryset(**kwargs)[start:end]
        return [obj async for obj in queryset]

    async def get_by_kwargs(self, **kwargs: Any) -> ModelType | None:
        """Retrieve a Django model instance by keyword arguments."""
        return await self.get_queryset(**kwargs).afirst()

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        """Create a new Django model instance from a Pydantic schema."""
        db_obj = self.model(**obj_in.model_dump())
        await db_obj.asave()
        return db_obj

    async def update(self, obj_id: int, obj_in: UpdateSchemaType) -> ModelType | None:
        """Update an existing Django model instance with new data."""
        if db_obj := await self.get(obj_id):
            for key, value in obj_in.model_dump(exclude_unset=True).items():
                setattr(db_obj, key, value)
            await db_obj.asave()
            return db_obj
        return None

    async def remove(self, obj_id: int) -> ModelType | None:
        """Remove a Django model instance by ID."""
        if db_obj := await self.get(obj_id):
            await db_obj.adelete()
            return db_obj
        return None
