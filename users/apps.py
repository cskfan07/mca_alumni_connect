
from django.apps import AppConfig

class UsersConfig(AppConfig):
    name = "users"

    def ready(self):
        from .mongo import init_mongo
        init_mongo()
