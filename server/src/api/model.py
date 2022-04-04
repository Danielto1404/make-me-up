from typing import List

import pydantic
from fastapi import UploadFile
from pydantic import BaseModel


class SignupParams(BaseModel):
    email: pydantic.EmailStr
    password: str = pydantic.Field(str, min_length=8)


class LoginParams(BaseModel):
    email: pydantic.EmailStr
    password: str = pydantic.Field(str, min_length=8)


class GenerateMakeRequestParams(BaseModel):
    truncation_psi: float = 0.75
    iterations: int = 1
    initial_iterations: int = 1
    batch_size: int = 1
    prompts: List[str]


class PhotoParams(BaseModel):
    file: UploadFile


class User(BaseModel):
    email: str
    token: str
