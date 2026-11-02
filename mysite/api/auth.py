from fastapi import APIRouter, HTTPException, Depends
from mysite.database.db import SessionLocal
from mysite.database.models import User, RefreshToken, UserRole
from mysite.schemas.auth_schema import UserInputSchema, UserLoginSchema
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from mysite.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_LIFETIME, REFRESH_TOKEN_LIFETIME
from datetime import timedelta, datetime
from jose import jwt, JWTError
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_LIFETIME)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    return create_access_token(data, expires_delta=timedelta(days=REFRESH_TOKEN_LIFETIME))

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
    except JWTError:
        raise HTTPException(detail='Токен неверный!', status_code=401)
    user_db = db.query(User).filter(User.username == username).first()
    if not user_db:
        raise HTTPException(detail='Пользователь не найден!', status_code=401)
    return user_db

async def get_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(detail='Нет доступа!', status_code=403)
    return current_user


@auth_router.post('/register', response_model=dict)
async def register(user: UserInputSchema, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.username == user.username).first()
    email_db = db.query(User).filter(User.email == user.email).first()
    if user_db or email_db:
        raise HTTPException(detail='Такой username или email уже есть!', status_code=400)

    hash_password = get_password_hash(user.password)
    user_data = User(
        username=user.username,
        email=user.email,
        password=hash_password,
        role=user.role,
    )
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return {'message': 'Регистрация прошла успешно!'}


@auth_router.post('/login/', response_model=dict)
async def login(user: UserLoginSchema, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.username == user.username).first()
    if not user_db or not verify_password(user.password, user_db.password):
        raise HTTPException(detail='Неверные данные!', status_code=400)

    access_token = create_access_token({'sub': user_db.username})
    refresh_token = create_refresh_token({'sub': user_db.username})

    token_db = RefreshToken(user_id=user_db.id, token=refresh_token)
    db.add(token_db)
    db.commit()

    return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'Bearer'}


@auth_router.post('/logout/', response_model=dict)
async def logout(refresh_token: str, db: Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not stored_token:
        raise HTTPException(status_code=401, detail='Токен неверный!')
    db.delete(stored_token)
    db.commit()
    return {'message': 'Вышли!'}


@auth_router.post('/refresh/', response_model=dict)
async def refresh(refresh_token: str, db: Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not stored_token:
        raise HTTPException(status_code=401, detail='Токен неверный!')
    access_token = create_access_token({'sub': stored_token.token_user.username})
    return {'access_token': access_token, 'token_type': 'Bearer'}
