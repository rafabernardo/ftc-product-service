from datetime import datetime

from adapters.models.page import Page
from models.product import Category
from pydantic import BaseModel, field_validator


class ProductIn(BaseModel):
    name: str
    category: str
    price: int
    description: str
    image: str

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str):
        try:
            Category(v)
            return v
        except ValueError:
            raise ValueError(f"Invalid category value: {v}")


class ProductUpdateIn(ProductIn):
    name: str | None = None
    category: str | None = None
    price: int | None = None
    description: str | None = None
    image: str | None = None


class ProductOut(ProductIn):
    id: int
    created_at: datetime
    updated_at: datetime


class PagedProductsOut(Page):
    results: list[ProductOut]
