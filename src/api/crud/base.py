from typing import Any, Generic, TypeVar
from uuid import UUID

from django.db import models
from django.db.models import QuerySet
from pydantic import BaseModel

from core.fastapi.exceptions import ObjectNotFoundException

__all__ = ["CRUDBase"]


ModelType = TypeVar("ModelType", bound=models.Model)
ReadSchemaType = TypeVar("ReadSchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
DeleteSchemaType = TypeVar("DeleteSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, ReadSchemaType, CreateSchemaType, UpdateSchemaType, DeleteSchemaType]):

    def __init__(
        self,
        model: type[ModelType],
        read_schema: type[ReadSchemaType],
        create_schema: type[CreateSchemaType] | None = None,
        update_schema: type[UpdateSchemaType] | None = None,
        delete_schema: type[DeleteSchemaType] | None = None,
    ) -> None:
        """Initialize the CRUDBase instance with a Django model and a Pydantic schema."""
        self.model = model
        self.read_schema = read_schema
        self.create_schema = create_schema
        self.update_schema = update_schema
        self.delete_schema = delete_schema

    def get_queryset(self) -> QuerySet[ModelType]:
        return self.model.objects.all()  # type: ignore

    async def get(self, pk: int | UUID | None = None, **kwargs: Any) -> ReadSchemaType:
        """Retrieve a Django model instance by ID and return it as a Pydantic schema."""
        if pk is None and not kwargs:
            raise ValueError("pk or kwargs must be provided")

        if pk:
            kwargs["id"] = pk

        if not (instance := await self.get_first(**kwargs)):
            raise ObjectNotFoundException(self.model.__name__)

        return self.read_schema.model_validate(instance)

    async def get_first(self, **kwargs: Any) -> ModelType | None:
        """Retrieve the first Django model instance that matches the given kwargs."""
        return await self.get_queryset().filter(**kwargs).afirst()

    async def list(self, skip: int = 0, limit: int = 100, **kwargs: Any) -> list[ReadSchemaType]:
        """Retrieve a list of Django model instances and return them as Pydantic schemas."""
        start, end = skip * limit, skip * limit + limit
        kwargs = {k: v for k, v in kwargs.items() if v is not None and v != ""}

        queryset: QuerySet[ModelType, ModelType] = self.get_queryset().filter(**kwargs)[start:end]

        if not await queryset.aexists():
            raise ObjectNotFoundException(self.model.__name__, plural=True)

        return [self.read_schema.model_validate(instance) async for instance in queryset]

    async def create(self, form: CreateSchemaType) -> CreateSchemaType:
        """Create a new Django model instance from a Pydantic schema."""
        instance = self.model(**form.model_dump())
        await instance.asave()

        if self.create_schema:
            return self.create_schema.model_validate(instance)

        raise ValueError("create_schema is not defined.")

    async def update(self, obj_id: int, form: UpdateSchemaType) -> UpdateSchemaType:
        """Update an existing Django model instance with new data."""
        if instance := await self.get_first(id=obj_id):
            for key, value in form.model_dump(exclude_unset=True).items():
                setattr(instance, key, value)
            await instance.asave()

            if self.update_schema:
                return self.update_schema.model_validate(instance)

            raise ValueError("update_schema is not defined.")
        raise ObjectNotFoundException(self.model.__name__)

    async def remove(self, obj_id: int) -> DeleteSchemaType:
        """Remove a Django model instance by ID."""
        if instance := await self.get_first(id=obj_id):
            await instance.adelete()

            if self.delete_schema:
                return self.delete_schema.model_validate(instance)

            raise ValueError("delete_schema is not defined.")
        raise ObjectNotFoundException(self.model.__name__)
