from sqlalchemy.orm import Session
from ..utils import hash_password
from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas
from ..database import get_db


router = APIRouter()


@router.post('', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = hash_password(user.password)
    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/{id}', response_model=schemas.UserResponse)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'User not found')

    return user
