from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas
from ..database import get_db
from ..oauth import get_current_user
from sqlalchemy import func


router = APIRouter()


@router.get('', response_model=List[schemas.PostResponse])
async def get_posts(db: Session = Depends(get_db), limit: Optional[int] = 10, page: Optional[int] = 1, search: Optional[str] = ""):
    skip = (page - 1) * limit
    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)).offset(skip).limit(limit).all()
    return posts


@router.get('/own', response_model=List[schemas.PostResponse])
async def get_own_posts(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(
        models.Post.user_id == current_user.id).all()
    return posts


@router.post('', status_code=status.HTTP_201_CREATED,
             response_model=schemas.PostResponse)
async def create_post(post: schemas.PostCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict(), user_id=current_user.id)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get('/{id}', response_model=schemas.PostResponse)
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post:
        return post
    raise HTTPException(status.HTTP_404_NOT_FOUND, 'Post not found')


@router.put('/{id}', response_model=schemas.PostResponse)
async def update_post(id, post: schemas.PostCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    query = db.query(models.Post).filter(models.Post.id == id)

    if query.first() and query.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perform this action')

    if query.first():
        query.update(post.dict())
        db.commit()
        return query.first()

    raise HTTPException(status.HTTP_404_NOT_FOUND, 'Post not found')


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    query = db.query(models.Post).filter(models.Post.id == id)
    if not query.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Post not found')

    if query.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perform this action')

    query.delete()
    db.commit()
    return
