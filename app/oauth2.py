from jose import jwt, JWTError
from . import schemas, models
from .database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from .database import settings

ACCESS_TOKEN_EXP = settings.access_token_exp
RESET_TOKEN_EXP = settings.reset_token_exp
ALGORITHM = settings.algorithm
SECRET_KEY = settings.secret_key

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# AT LOGIN CREATE THE TOKEN
def create_token(data: dict):
    to_encode = data.copy()
    expre_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXP)
    to_encode.update({"exp": expre_time})
    
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    
    return encoded_jwt

def verify_token(token: str, cred_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        
        if id is None:
            raise cred_exception
        
        token_data = schemas.TokenData(id=id)
    
    except JWTError:
        raise cred_exception
        
        
    return token_data
              

def get_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    cred_exception = HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Unauthorized.", headers={"WWW-Authenticate": "Bearer"})
    
    token_data = verify_token(token, cred_exception)
    
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    
    return user

def create_reset_token(data: dict):
    to_encode = data.copy()
    expre_time = datetime.now(timezone.utc) + timedelta(minutes=RESET_TOKEN_EXP)
    to_encode.update({"exp": expre_time})
    
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    
    return encoded_jwt
    
def verify_reset_token(token: str):
    cred_exception = HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail='Password reset not accessible.')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        
        if email is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found.")
    
    except JWTError:
        raise cred_exception
        
    return email
    
    
    


    
    
    
    

