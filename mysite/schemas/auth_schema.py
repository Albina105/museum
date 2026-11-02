from pydantic import BaseModel
from mysite.database.models import UserRole


class UserInputSchema(BaseModel):
    username: str
    email: str
    password: str
    role: UserRole = UserRole.visitor

class UserLoginSchema(BaseModel):
    username: str
    password: str
