from unittest.mock import AsyncMock, patch

import httpx
import pytest
from fastapi import HTTPException

from external.authentication import validate_token


@pytest.mark.asyncio
async def test_validate_token_success():
    token = "valid_token"
    expected_response = {"user_id": 123, "role": "admin"}

    mock_response = httpx.Response(
        status_code=200,
        json=expected_response,
        request=httpx.Request("GET", "test"),
    )

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_response

        result = await validate_token(token)

    assert result == expected_response


@pytest.mark.asyncio
async def test_validate_token_error():
    token = "valid_token"

    mock_response = httpx.Response(
        401,
        json="Invalid token",
        request=httpx.Request("GET", "test"),
    )

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_response
        with pytest.raises(HTTPException, match="Invalid token"):
            await validate_token(token)


@pytest.mark.asyncio
async def test_validate_token_error_exception():
    token = "valid_token"

    httpx.Response(500, json="Invalid token")

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        try:
            mock_get.side_effect = Exception
            await validate_token(token)
        except HTTPException as ex:
            assert ex.status_code == 500
