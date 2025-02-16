from unittest.mock import AsyncMock, patch

import httpx
import pytest

from external.authentication import validate_token


@pytest.mark.asyncio
async def test_validate_token_success():
    token = "valid_token"
    expected_response = {"user_id": 123, "role": "admin"}

    mock_response = httpx.Response(200, json=expected_response)

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_response

        result = await validate_token(token)

    assert result == expected_response


@pytest.mark.asyncio
async def test_validate_token_error():
    token = "valid_token"

    mock_response = httpx.Response(401, json="Invalid token")

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_response

        result = await validate_token(token)

    assert result == "Invalid token"
