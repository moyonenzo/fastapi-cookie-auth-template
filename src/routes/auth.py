import os, re

from fastapi import APIRouter, Depends, status, HTTPException, Response, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr, Field, validator
from sqlalchemy.orm import Session
from PIL import Image

import src.models as models
import src.utils as utils

from src.database import get_db

router = APIRouter()


class RegisterPayload(BaseModel):
    username: str = Field(pattern=r"[a-zA-Z0-9_-]")
    email: EmailStr
    password: str

    @validator("password")
    def validate_password(cls, value):
        regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\W)(?=.{8,}).*$"
        if not re.match(regex, value):
            raise ValueError(
                "Password must contain at least 8 characters, including an uppercase letter, a lowercase letter, and a special character."
            )
        return value


class LoginPayload(BaseModel):
    email: EmailStr
    password: str


@router.get("/", status_code=status.HTTP_200_OK)
def auth(identity: str | None = Depends(utils.get_identity)):
    if identity is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return identity


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(body: RegisterPayload, db: Session = Depends(get_db)):
    user = db.query(models.Users).where(models.Users.email == body.email).first()
    if user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    user = models.Users(
        username=body.username,
        email=body.email,
        password=utils.hash_password(body.password),
    )

    db.add(user)
    db.commit()


@router.post("/login", status_code=status.HTTP_200_OK)
def login(body: LoginPayload, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.Users).where(models.Users.email == body.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if not utils.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    token = utils.create_access_token(user)
    response.set_cookie(
        key="authenticator", value=token, max_age=24 * 3600, secure=False, httponly=True
    )

    return utils.retrieve_access_token(token)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response, identity: str | None = Depends(utils.get_identity)):
    if identity is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    response.delete_cookie("authenticator")
