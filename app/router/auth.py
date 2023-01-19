from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, models, utils, oauth2
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix='/login',
    tags=["Login"]
)


@router.post('/', response_model=schemas.Token)
def login(login_user: schemas.UserBase, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == login_user.email).first()

    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail='User not found.')

    if not user or not utils.verify_pwd(login_user.password, user.password):
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,
                            detail="Username and password not match.")

    access_token = oauth2.create_token({"user_id": user.id})

    return {"access_token": access_token,
            "token_type": "bearer"}


@router.post('/forgot')
def forgot_password(cred_user: schemas.ForgotPassword, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(
        models.User.email == cred_user.email).first()
    print(user is None)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail='User not found.')

    reset_token = oauth2.create_reset_token({"email": user.email})

    try:
        utils.send_token(user.email, reset_token)
    except:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail=f'Could not send the email to {user.email}')

    return {"message": f"Email sent to {user.email}. Token valid for 10 minutes."}


@router.post('/reset_password')
def reset_password(user_data: schemas.ResetPassword, db: Session = Depends(get_db)):

    email = oauth2.verify_reset_token(user_data.access_token)

    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='User not found')

    user.password = utils.hash(user_data.password)
    db.commit()

    return {"message": f"Password of {user.email} is successfully changed."}
