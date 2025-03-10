from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from pytest_bdd import given, parsers, scenarios, then, when

from api.v1.users import router
from core.dependency_injection import Container
from services.user_service import UserService

client = TestClient(router)

scenarios("../../features/user_identify_sucess.feature")


@pytest.fixture
def user_service_mock():
    return Mock(spec=UserService)


@pytest.fixture
def container(user_service_mock):
    container = Container()
    container.user_service.override(user_service_mock)
    return container


@pytest.fixture(autouse=True)
def setup(container):
    container.init_resources()
    container.wire(modules=[__name__])
    yield
    container.unwire()


@pytest.fixture
def context():
    return {}


@given(parsers.parse('a user with id "{user_id}"'))
def user_id(context, user_id):
    context["user_id"] = user_id


@when(parsers.parse('the user wants to add their CPF "{cpf}"'))
def add_cpf(context, user_service_mock, cpf, user_mock):
    user_id = context["user_id"]

    # Mock the service response
    user_service_mock.identify_user.return_value = user_mock

    # Make the request
    request_data = {"cpf": cpf}
    response = client.patch(f"users/identify/{user_id}", json=request_data)

    context["response"] = response
    context["expected_cpf"] = user_mock.cpf


@then(parsers.parse('the user should have the CPF "{cpf}"'))
def check_cpf(context, cpf):
    assert context["expected_cpf"] == cpf


@then(parsers.parse("the response status code should be {status_code:d}"))
def check_status_code(context, status_code):
    assert context["response"].status_code == status_code
