import httpx
from fastapi import HTTPException, status

from core.settings import get_settings

settings = get_settings()


async def validate_token(token: str) -> dict:
    # URL of the token validation endpoint in the other microservice
    validate_token_url = (
        f"http://{settings.AUTHENTICATION_URL}/service/v1/validate-token"
    )
    print(validate_token_url)
    # Make a request to the other microservice
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                validate_token_url,
                headers={"Authorization": f"Bearer {token}"},
            )
            if response.status_code == 200:
                return response.json()  # Return the validated token payload

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to validate token",
            ) from e
