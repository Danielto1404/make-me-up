from fastapi import APIRouter
from fastapi import HTTPException
from firebase_admin import auth
from firebase_admin.auth import UserNotFoundError
from firebase_admin.exceptions import FirebaseError

from src.api.handlers import AuthHandler
from src.api.model import SignupParams, LoginParams

router = APIRouter(prefix="/auth")

auth_handler = AuthHandler()


@router.post("/signup")
async def signup(params: SignupParams):
    try:
        hashed_password = auth_handler.get_password_hash(params.password)
        user = auth.create_user(email=params.email, password=hashed_password)
        token = auth.create_custom_token(uid=user.uid, developer_claims={
            "email": True,
            "uid": True
        })
        print(token)
        return {"token": token}
    except FirebaseError:
        return HTTPException(status_code=403, detail="User is already exits")
    except ValueError:
        return HTTPException(status_code=403, detail="Fields are invalid")


@router.post("/login")
async def login(params: LoginParams):
    try:
        user = auth.get_user_by_email(params.email)
        token = auth_handler.encode_token(user.uid)
        return {"token": token}
    except UserNotFoundError:
        return HTTPException(status_code=403, detail="User is not exists")
    except FirebaseError:
        return HTTPException(status_code=402, detail="Unable to fetch user")
