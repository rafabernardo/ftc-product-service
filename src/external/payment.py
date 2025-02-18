import httpx
from fastapi import HTTPException, status

from core.settings import get_settings

settings = get_settings()


async def register_payment(token: str, payload: dict) -> dict:
    # URL of the token validation endpoint in the other microservice
    payment_url = f"http://{settings.PAYMENT_URL}/v1/payments/"

    # Make a request to the other microservice
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                payment_url,
                headers={"Authorization": f"Bearer {token}"},
                json=payload,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.text,
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to validate token",
            ) from e
