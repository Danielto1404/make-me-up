import firebase_admin
from firebase_admin import credentials

from ..store import config

key_path = config["firebase"]["key-path"]
storage_bucket = config["firebase"]["storage-bucket"]

cred = credentials.Certificate(key_path)
firebase = firebase_admin.initialize_app(cred, {
    "storageBucket": storage_bucket
})
