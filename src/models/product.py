from datetime import datetime
from enum import Enum

from pydantic import BaseModel, field_validator


class Category(Enum):
    meal = "meal"
    side_dish = "side-dish"
    beverage = "beverage"
    dessert = "dessert"


class BaseProduct(BaseModel):
    name: str
    category: str
    price: int
    description: str
    image: str


class Product(BaseProduct):
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str):
        try:
            Category(v)
            return v
        except ValueError as e:
            raise ValueError(f"Invalid category value: {v}") from e
