from adapters.models.page import Page


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
