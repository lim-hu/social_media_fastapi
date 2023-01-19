from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, utils
from ..database import get_db
from typing import List

router = APIRouter(
    prefix='/users',
    tags=['User']
)

# GET ALL USER
@router.get('/', response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    
    return users

# CREATE USER
@router.post('/', response_model=schemas.User)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    
    user = db.query(models.User).filter(models.User.email == user.email).first()
    
    if user:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail='User already exists.')
    
    new_user.password = utils.hash(new_user.password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

# GET USER
@router.post('/', response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='User not found.')
        
    return user

