from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from api.v1.exceptions.commons import (
    InternalServerErrorHTTPException,
    NoDocumentsFoundHTTPException,
)
from api.v1.models.product import (
    ListProductV1Response,
    ProductPatchV1Request,
    ProductV1Request,
    ProductV1Response,
)
from core.dependency_injection import Container
from core.exceptions.commons_exceptions import NoDocumentsFoundException
from external.authentication import validate_token
from models.product import Category, Product
from repositories.utils import clean_up_dict, get_pagination_info
from services.product_service import ProductService

HEADER_CONTENT_TYPE = "content-type"
HEADER_CONTENT_TYPE_APPLICATION_JSON = "application/json"

router = APIRouter(prefix="/products")


@router.get("/", response_model=ListProductV1Response)
@inject
async def list_products(
    response: Response,
    page: int = Query(default=1, gt=0),
    page_size: int = Query(default=10, gt=0, le=100),
    category: Category = Query(None),  # noqa: B008
    product_service: ProductService = Depends(  # noqa: B008
        Provide[Container.product_service]
    ),
    auth: HTTPAuthorizationCredentials = Depends(HTTPBearer()),  # noqa: B008
):
    try:
        token = auth.credentials
        await validate_token(token)

        filter_prod = {}
        if category:
            filter_prod["category"] = category.value

        products = product_service.list_products(
            filter_prod=filter_prod,
            page=page,
            page_size=page_size,
        )
        total_products = product_service.count_products(filter_prod=filter_prod)

        pagination_info = get_pagination_info(
            total_results=total_products, page=page, page_size=page_size
        )

        listed_products = [
            ProductV1Response(**product.model_dump()) for product in products
        ]

        paginated_orders = ListProductV1Response(
            **pagination_info.model_dump(), results=listed_products
        )

        response.status_code = status.HTTP_200_OK
        response.headers[HEADER_CONTENT_TYPE] = (
            HEADER_CONTENT_TYPE_APPLICATION_JSON
        )

        return paginated_orders
    except Exception as exc:
        raise InternalServerErrorHTTPException() from exc


@router.get("/{product_id}", response_model=ProductV1Response)
@inject
async def get_product_by_id(
    product_id: str,
    response: Response,
    product_service: ProductService = Depends(  # noqa: B008
        Provide[Container.product_service]
    ),
    auth: HTTPAuthorizationCredentials = Depends(HTTPBearer()),  # noqa: B008
):
    try:
        token = auth.credentials
        await validate_token(token)
        product = product_service.get_product_by_id(product_id)
    except Exception as exc:
        raise InternalServerErrorHTTPException() from exc

    if not product:
        raise NoDocumentsFoundHTTPException()
    response.status_code = status.HTTP_200_OK
    response.headers[HEADER_CONTENT_TYPE] = HEADER_CONTENT_TYPE_APPLICATION_JSON

    return product


@router.post("", response_model=ProductV1Response)
@inject
async def register(
    create_product_request: ProductV1Request,
    response: Response,
    product_service: ProductService = Depends(  # noqa: B008
        Provide[Container.product_service]
    ),
    auth: HTTPAuthorizationCredentials = Depends(HTTPBearer()),  # noqa: B008
):
    try:
        token = auth.credentials
        await validate_token(token)
        product = Product(**create_product_request.model_dump())
        product = product_service.register_product(product)
        response.status_code = status.HTTP_201_CREATED
        response.headers[HEADER_CONTENT_TYPE] = (
            HEADER_CONTENT_TYPE_APPLICATION_JSON
        )

        return product
    except Exception as exc:
        raise InternalServerErrorHTTPException() from exc


@router.delete("/{product_id}")
@inject
async def delete(
    product_id: str,
    response: Response,
    product_service: ProductService = Depends(  # noqa: B008
        Provide[Container.product_service]
    ),
    auth: HTTPAuthorizationCredentials = Depends(HTTPBearer()),  # noqa: B008
):
    try:
        token = auth.credentials
        await validate_token(token)
        product_service.delete_product(product_id)
    except NoDocumentsFoundException as exc:
        raise NoDocumentsFoundHTTPException() from exc
    except Exception as exc:
        raise InternalServerErrorHTTPException() from exc

    response.status_code = status.HTTP_204_NO_CONTENT
    response.headers[HEADER_CONTENT_TYPE] = HEADER_CONTENT_TYPE_APPLICATION_JSON


@router.patch("/{product_id}", response_model=ProductV1Response)
@inject
async def update(
    product_id: str,
    product_request: ProductPatchV1Request,
    response: Response,
    product_service: ProductService = Depends(  # noqa: B008
        Provide[Container.product_service]
    ),
    auth: HTTPAuthorizationCredentials = Depends(HTTPBearer()),  # noqa: B008
):
    try:
        token = auth.credentials
        await validate_token(token)
        cleaned_product_request = clean_up_dict(product_request.model_dump())
        product = product_service.update_product(
            product_id, **cleaned_product_request
        )

        response.status_code = status.HTTP_200_OK
        response.headers[HEADER_CONTENT_TYPE] = (
            HEADER_CONTENT_TYPE_APPLICATION_JSON
        )

        return product
    except NoDocumentsFoundException as exc:
        raise NoDocumentsFoundHTTPException() from exc
    except Exception as exc:
        raise InternalServerErrorHTTPException() from exc
