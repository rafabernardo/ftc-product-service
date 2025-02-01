from adapters.models.page import Page
from adapters.models.product import PagedProductsOut, ProductOut
from models.product import Product


class ProductAdapter:
    def adapt_pagineted_products(
        self, products: list[Product], total_products: int, page: int, page_size: int
    ):
        pagination_info = self.get_pagination_info(
            total_results=total_products, page=page, page_size=page_size
        )
        listed_products = [ProductOut(**product.model_dump()) for product in products]

        pagineted_products = PagedProductsOut(
            **pagination_info.model_dump(), results=listed_products
        )
        return pagineted_products

    @staticmethod
    def get_pagination_info(total_results=int, page=int, page_size=int) -> Page:
        total_pages = (total_results + page_size - 1) // page_size
        has_next = page < total_pages
        has_previous = page > 1

        pagination_info = Page(
            total_results=total_results,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=has_next,
            has_previous=has_previous,
        )
        return pagination_info
