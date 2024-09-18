import structlog
from typing import Annotated

from fastapi import Cookie

from src.utils.webtokens import (
    create_access_token,
    retrieve_access_token,
    hash_password,
    verify_password,
    logged_as,
)

logger = structlog.get_logger(__name__)


async def get_authenticator(authenticator: Annotated[str | None, Cookie()] = None):
    if authenticator is None:
        return None

    return retrieve_access_token(authenticator)
