from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models
from ..oauth2 import get_user
from ..database import get_db

router = APIRouter(
    prefix='/votes',
    tags=['Vote']
)


@router.post('/')
def vote(vote: schemas.PostVote, db: Session = Depends(get_db), current_user=Depends(get_user),):
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status.HTTP_409_CONFLICT, detail='You have already voted this post!')
        
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        
        return {"message": "Vote added."}
    
    else:
        if not found_vote:
            raise HTTPException(status.HTTP_409_CONFLICT, detail='Vote does not exists!')
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        
        return {"message": "Vote deleted."} 
    