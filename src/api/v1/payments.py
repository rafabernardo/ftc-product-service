from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict

from api.v1.exceptions.commons import NoDocumentsFoundHTTPException
from core.dependency_injection import Container
from core.exceptions.commons_exceptions import NoDocumentsFoundException
from services.order_service import OrderService

HEADER_CONTENT_TYPE = "content-type"
HEADER_CONTENT_TYPE_APPLICATION_JSON = "application/json"

router = APIRouter(prefix="/payments")


class PaymentRequest(BaseModel):
    model_config = ConfigDict(extra="allow")


@router.post("/{order_id}")
@inject
async def set_payment_status(
    order_id: str,
    response: Response,
    payment_data: PaymentRequest,
    order_service: OrderService = Depends(  # noqa: B008
        Provide[Container.order_service],
    ),
):
    try:
        payment_data = payment_data.model_dump()
        payment_result = payment_data.get("status") == "success"
        order_service.set_payment_status(order_id, payment_result)

    except NoDocumentsFoundException as exc:
        raise NoDocumentsFoundHTTPException() from exc

    response.status_code = status.HTTP_204_NO_CONTENT
    response.headers[HEADER_CONTENT_TYPE] = HEADER_CONTENT_TYPE_APPLICATION_JSON
