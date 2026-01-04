from mongoengine import connect
import os

def init_mongo():
    connect(
        db=os.environ["MONGO_DB_NAME"],
        host=os.environ["MONGO_URI"],
        alias="default",
        uuidRepresentation="standard",
        serverSelectionTimeoutMS=5000
    )
