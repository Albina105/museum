from .views import UserAdmin, RefreshTokenAdmin, ExhibitAdmin

from fastapi import FastAPI
from sqladmin import Admin
from mysite.database.db import engine


def setup_admin(museum_app: FastAPI):
    admin = Admin(museum_app, engine)
    admin.add_view(UserAdmin)
    admin.add_view(RefreshTokenAdmin)
    admin.add_view(ExhibitAdmin)
