import os

from dotenv import load_dotenv
from fastapi.testclient import TestClient
from passlib.context import CryptContext
from jose import jwt

import src.models as models

load_dotenv()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(user: models.Users) -> str:
    data = {"id": user.id, "username": user.username, "email": user.email}

    encoded = jwt.encode(data, os.getenv("SECRET_KEY"), algorithm="HS256")
    return encoded


def retrieve_access_token(token: str) -> dict:
    return jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


class logged_as(object):
    def __init__(self, client: TestClient, user: models.Users):
        self.client = client
        self.token = create_access_token(user)

    def __enter__(self):
        self.client.cookies = {"authenticator": self.token}

    def __exit__(self, *args):
        self.client.cookies = None
