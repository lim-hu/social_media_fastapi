from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models
from ..oauth2 import get_user
from ..database import get_db
from typing import List

router = APIRouter(
    prefix='/posts',
    tags=['Post']
)

@router.get('/', response_model=List[schemas.Post])
def get_posts(current_user = Depends(get_user), db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    
    return posts

@router.post('/', response_model=schemas.Post)
def create_post(post: schemas.PostBase, db: Session = Depends(get_db), current_user = Depends(get_user),):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    
    post = db.query(models.Post).filter(models.Post.title == post.title).first()

    if post:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail='Post title already exists.')
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostBase, db: Session = Depends(get_db), current_user = Depends(get_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Post not found.')
    
    if post.owner_id != current_user.id:
        raise HTTPException(status.HTTP_405_METHOD_NOT_ALLOWED, detail='You are not the owner of this post.')
    
    post_query.update(updated_post.dict())
    post = post_query.first()
    db.commit()
    db.refresh(post)
    
    return post   

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, current_user = Depends(get_user), db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Post not found.')
    
    if post.owner_id != current_user.id:
        raise HTTPException(status.HTTP_405_METHOD_NOT_ALLOWED, detail='You ar not the owner of this post.')
    
    post_query.delete(synchronize_session=False)
    db.commit()
        

@router.post('/', response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Post not found.')
        
    return post
