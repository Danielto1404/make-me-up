from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, UploadFile
from fastapi.security import OAuth2PasswordBearer
from firebase_admin.exceptions import FirebaseError

from src.api.model import User

router = APIRouter(prefix="/me")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def fake_decode_token(token):
    return User(
        email="john@example.com", token=token
    )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user


@router.get("/photos")
async def get_user_photos(user: User = Depends(get_current_user)):
    try:
        print(user)
    except FirebaseError:
        return HTTPException(status_code=403, detail="User is already exits")
    except ValueError:
        return HTTPException(status_code=403, detail="Fields are invalid")


@router.post("/upload/")
async def create_upload_file(file: Optional[UploadFile]):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}
