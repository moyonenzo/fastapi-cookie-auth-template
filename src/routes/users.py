import os
import enum

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from PIL import Image

import src.utils as utils

router = APIRouter()


class PhotoSize(enum.Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


def save_with_size(file, size: tuple[int, int], save_path: str):
    image = Image.open(file)
    image.thumbnail(size, Image.LANCZOS)
    image.save(save_path)


@router.get("/{user_id}/photo", status_code=status.HTTP_200_OK)
def get_user_photo(user_id: int, size: PhotoSize = PhotoSize.MEDIUM):
    path = f"/app/public/photos/{user_id}-{size.value}.jpeg"
    print(path)
    if not os.path.exists(path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return FileResponse(path, media_type="image/jpeg")


@router.post("/{user_id}/photo", status_code=status.HTTP_201_CREATED)
def set_user_photo(
    user_id: int,
    photo: UploadFile,
    authenticator: str | None = Depends(utils.get_authenticator),
):
    if authenticator is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if authenticator["id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    extension = photo.content_type
    if extension not in ["image/jpeg", "image/jpg"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    save_with_size(photo.file, (128, 128), f"/app/public/photos/{user_id}-small.jpeg")
    save_with_size(photo.file, (256, 256), f"/app/public/photos/{user_id}-medium.jpeg")
    save_with_size(photo.file, (512, 512), f"/app/public/photos/{user_id}-large.jpeg")
