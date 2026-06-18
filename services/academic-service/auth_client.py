import os

import requests


AUTH_URL = os.getenv(
    "AUTH_SERVICE_URL",
    "http://auth-service:8000"
)


def validate_token(token):
    try:
        response = requests.post(
            f"{AUTH_URL}/validate",
            json={"token": token},
            timeout=5
        )

        return response.json()

    except Exception:
        return {"valid": False}