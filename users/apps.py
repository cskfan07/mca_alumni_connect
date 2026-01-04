from django.apps import AppConfig
import os
from mongoengine import connect

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        """
        MongoEngine connect after Django process fork.
        Safe for Render / gunicorn multi-process.
        """
        MONGO_URI = os.getenv("MONGO_URI")
        MONGO_DB = os.getenv("MONGO_DB_NAME")
        if MONGO_URI and MONGO_DB:
            connect(db=MONGO_DB, host=MONGO_URI)
