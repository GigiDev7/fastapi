from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas
from ..database import get_db
from ..oauth import get_current_user


router = APIRouter()


@router.post('', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.direction == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail='You already voted on this post')

        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {'message': 'successfully added vote'}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Vote not found')

        vote_query.delete()
        db.commit()
        return {'message': 'successfully deleted vote'}
