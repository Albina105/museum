from mysite.database.models import User, RefreshToken, Exhibit

from sqladmin import ModelView


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email, User.role]

class RefreshTokenAdmin(ModelView, model=RefreshToken):
    column_list = [RefreshToken.id, RefreshToken.user_id, RefreshToken.created_at]

class ExhibitAdmin(ModelView, model=Exhibit):
    column_list = [Exhibit.id, Exhibit.title, Exhibit.origin]
