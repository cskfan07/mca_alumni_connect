from django.apps import AppConfig
import os
from mongoengine import connect, connection

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        MONGO_URI = os.getenv("MONGO_URI")
        MONGO_DB = os.getenv("MONGO_DB_NAME")

        if MONGO_URI and MONGO_DB:
            if 'default' not in connection._connections:
                connect(
                    db=MONGO_DB,
                    host=MONGO_URI,
                    alias='default',
                    connect=False   # 🔥 VERY IMPORTANT
                )
