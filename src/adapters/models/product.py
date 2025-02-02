from datetime import datetime

from adapters.models.page import Page
from models.product import BaseProduct


class ProductIn(BaseProduct): ...


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
