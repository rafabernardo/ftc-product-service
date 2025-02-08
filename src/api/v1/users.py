from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response, status

from api.v1.exceptions.commons import (
    InternalServerErrorHTTPException,
    NoDocumentsFoundHTTPException,
    UnprocessableEntityErrorHTTPException,
)
from api.v1.models.user import (
    IdentifyUserV1Request,
    RegisterUserV1Request,
    UserV1Response,
)
from core.dependency_injection import Container
from core.exceptions.commons_exceptions import NoDocumentsFoundException
from core.exceptions.user_exceptions import (
    UserAlreadyExistsError,
    UserInvalidFormatDataError,
)
from models.user import User
from services.user_service import UserService

HEADER_CONTENT_TYPE = "content-type"
HEADER_CONTENT_TYPE_APPLICATION_JSON = "application/json"

router = APIRouter(prefix="/users")


@router.get("", response_model=list[UserV1Response])
@inject
async def list_users(
    response: Response,
    user_service: UserService = Depends(  # noqa: B008
        Provide[Container.user_service]
    ),
):
    try:
        users = user_service.list_users()
    except Exception as exc:
        raise InternalServerErrorHTTPException() from exc

    response.status_code = status.HTTP_200_OK
    response.headers[HEADER_CONTENT_TYPE] = (
        HEADER_CONTENT_TYPE_APPLICATION_JSON
    )

    return users


@router.get("/{user_id}", response_model=UserV1Response)
@inject
async def get_user_by_id(
    user_id: str,
    response: Response,
    user_service: UserService = Depends(  # noqa: B008,
        Provide[Container.user_service]
    ),
):
    try:
        user = user_service.get_user_by_id(user_id)
    except Exception as exc:
        raise InternalServerErrorHTTPException() from exc

    if not user:
        raise NoDocumentsFoundHTTPException()
    response.status_code = status.HTTP_200_OK
    response.headers[HEADER_CONTENT_TYPE] = (
        HEADER_CONTENT_TYPE_APPLICATION_JSON
    )

    return user


@router.get("/cpf/{cpf}", response_model=UserV1Response)
@inject
async def get_user_by_cpf(
    cpf: str,
    response: Response,
    user_service: UserService = Depends(  # noqa: B008
        Provide[Container.user_service]
    ),
):
    try:
        user = user_service.get_user_by_cpf(cpf)

    except UserInvalidFormatDataError as exc:
        raise UnprocessableEntityErrorHTTPException(
            detail=exc.message,
        ) from exc
    except Exception as exc:
        raise InternalServerErrorHTTPException() from exc

    if user is None:
        raise NoDocumentsFoundHTTPException()

    response.status_code = status.HTTP_200_OK
    response.headers[HEADER_CONTENT_TYPE] = (
        HEADER_CONTENT_TYPE_APPLICATION_JSON
    )

    return user


@router.post("/register", response_model=UserV1Response)
@inject
async def register(
    create_user_request: RegisterUserV1Request,
    response: Response,
    user_service: UserService = (
        Depends(Provide[Container.user_service])  # noqa: B008
    ),
):
    try:
        user = User(**create_user_request.model_dump())

        created_user = user_service.register_user(user)
    except UserAlreadyExistsError as exc:
        raise NoDocumentsFoundHTTPException(detail=exc.message) from exc
    except UserInvalidFormatDataError as exc:
        raise UnprocessableEntityErrorHTTPException(
            detail=exc.message
        ) from exc
    except Exception as exc:
        raise InternalServerErrorHTTPException() from exc

    response.status_code = status.HTTP_201_CREATED
    response.headers[HEADER_CONTENT_TYPE] = (
        HEADER_CONTENT_TYPE_APPLICATION_JSON
    )

    return created_user


@router.delete("/delete/{user_id}")
@inject
async def delete(
    user_id: str,
    response: Response,
    user_service: UserService = Depends(  # noqa: B008
        Provide[Container.user_service]
    ),
):
    try:
        was_user_deleted = user_service.delete_user(user_id)

        if was_user_deleted:
            response.status_code = status.HTTP_204_NO_CONTENT
            return

        raise InternalServerErrorHTTPException()

    except NoDocumentsFoundException as exc:
        raise NoDocumentsFoundHTTPException() from exc
    except Exception as exc:
        raise InternalServerErrorHTTPException() from exc


@router.patch("/identify/{user_id}", response_model=UserV1Response)
@inject
async def identify_user(
    user_id: str,
    identify_user_request: IdentifyUserV1Request,
    response: Response,
    user_service: UserService = Depends(  # noqa: B008
        Provide[Container.user_service]
    ),
):
    try:
        updated_user = user_service.identify_user(
            user_id, identify_user_request.cpf
        )

        response.status_code = status.HTTP_200_OK
        response.headers[HEADER_CONTENT_TYPE] = (
            HEADER_CONTENT_TYPE_APPLICATION_JSON
        )

        return updated_user

    except NoDocumentsFoundException as exc:
        raise NoDocumentsFoundHTTPException() from exc
    except UserInvalidFormatDataError as exc:
        raise UnprocessableEntityErrorHTTPException(exc.message) from exc
    except UserAlreadyExistsError as exc:
        raise UnprocessableEntityErrorHTTPException(exc.message) from exc
    except Exception as exc:
        raise InternalServerErrorHTTPException() from exc
