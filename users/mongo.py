from mongoengine import connect
import os

_connected = False

def init_mongo():
    global _connected
    if _connected:
        return

    MONGO_URI = os.environ.get("MONGO_URI")
    MONGO_DB = os.environ.get("MONGO_DB_NAME")

    if not MONGO_URI or not MONGO_DB:
        raise Exception("MongoDB environment variables missing")

    connect(
        db=MONGO_DB,
        host=MONGO_URI,
        alias="default"
    )

    _connected = True
