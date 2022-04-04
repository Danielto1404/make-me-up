import firebase_admin
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import credentials

from src.api import api
from src.store import config

app = FastAPI()
app.include_router(router=api)

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

key_path = config["firebase"]["key-path"]
storage_bucket = config["firebase"]["storage-bucket"]

cred = credentials.Certificate(key_path)
firebase = firebase_admin.initialize_app(cred, {
    "storageBucket": storage_bucket
})