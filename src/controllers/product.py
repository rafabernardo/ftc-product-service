from adapters.models.product import (
    PagedProductsOut,
    ProductIn,
    ProductOut,
    ProductUpdateIn,
)
from adapters.product import ProductAdapter
from models.product import Category
from use_cases.product import ProductUseCases


class ProductController:
    @staticmethod
    def pagineted_products(
        page: int,
        page_size: int,
        category: Category,
    ) -> PagedProductsOut:
        filters = {}
        if category:
            filters["category"] = category.value

        products = ProductUseCases().list_products(
            filters=filters, page=page, page_size=page_size
        )
        total_products = ProductUseCases().get_total_products(filters=filters)

        pagineted_products = ProductAdapter.adapt_pagineted_products(
            products=products,
            total_products=total_products,
            page=page,
            page_size=page_size,
        )

        return pagineted_products

    @staticmethod
    def get_product_by_id(product_id: int) -> ProductOut:
        pass

    @staticmethod
    def create_product(product: ProductIn) -> ProductOut:
        pass

    @staticmethod
    def update_product(product: ProductUpdateIn) -> ProductOut:
        pass

    @staticmethod
    def delete_product(product_id: int) -> None:
        pass
