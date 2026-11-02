from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.api.auth import get_admin
from mysite.database.db import SessionLocal
from mysite.database.models import Exhibit, User
from mysite.schemas.exhibit_schema import ExhibitInputSchema, ExhibitOutSchema

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


home_router = APIRouter(tags=['Home'])

exhibit_router = APIRouter(prefix='/exhibits', tags=['Exhibit'])

@home_router.get('/', response_model=dict)
async def home():
    return {'message': 'AI-Музей: виртуальный гид работает!'}


@exhibit_router.post('/', response_model=ExhibitOutSchema)
async def create_exhibit(exhibit: ExhibitInputSchema, db: Session = Depends(get_db),
                         admin: User = Depends(get_admin)):
    exhibit_db = Exhibit(**exhibit.dict())
    db.add(exhibit_db)
    db.commit()
    db.refresh(exhibit_db)
    return exhibit_db

@exhibit_router.get('/', response_model=List[ExhibitOutSchema])
async def list_exhibits(db: Session = Depends(get_db)):
    return db.query(Exhibit).all()

@exhibit_router.get('/{exhibit_id}', response_model=ExhibitOutSchema)
async def get_exhibit(exhibit_id: int, db: Session = Depends(get_db)):
    exhibit_db = db.query(Exhibit).filter(Exhibit.id == exhibit_id).first()
    if not exhibit_db:
        raise HTTPException(detail='Exhibit not found', status_code=404)
    return exhibit_db

@exhibit_router.put('/{exhibit_id}', response_model=dict)
async def update_exhibit(exhibit_id: int, exhibit: ExhibitInputSchema, db: Session = Depends(get_db),
                         admin: User = Depends(get_admin)):
    exhibit_db = db.query(Exhibit).filter(Exhibit.id == exhibit_id).first()
    if not exhibit_db:
        raise HTTPException(detail='Exhibit not found', status_code=404)
    for exhibit_key, exhibit_value in exhibit.dict().items():
        setattr(exhibit_db, exhibit_key, exhibit_value)
    db.commit()
    db.refresh(exhibit_db)
    return {'message': 'Exhibit был успешно изменен!'}

@exhibit_router.delete('/{exhibit_id}', response_model=dict)
async def delete_exhibit(exhibit_id: int, db: Session = Depends(get_db),
                         admin: User = Depends(get_admin)):
    exhibit_db = db.query(Exhibit).filter(Exhibit.id == exhibit_id).first()
    if not exhibit_db:
        raise HTTPException(detail='Exhibit not found', status_code=404)
    db.delete(exhibit_db)
    db.commit()
    return {'message': 'Exhibit был успешно удален!'}
