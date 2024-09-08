from sqlmodel import SQLModel,select,Session
from fastapi import FastAPI,HTTPException,Depends
from passlib.context import CryptContext
from datetime import datetime,timedelta
import jwt
from typing import Optional
from models import User

pwd_context=CryptContext(schemes=["bcrypt"],depracated="auto")

SECRET_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
ALGORITHM="HS256"
ACCESS_TOKEN_EXP_MIN=15
REFRESH_TOKEN_EXP_DAY=30
async def hashing_password(password: str):
    return pwd_context.hash(password)

async def create_user(name:str ,password,session:Session):
    user = User(name=name,hashed_password=hashing_password(password=password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

async def sign_up(name: str,password: str,session: Session):
    user = session.exec(select(User).where(User.name==name)).first()
    if not user:
        create_user(name=name,password=password,session=session)
    else:
        raise HTTPException(status_code=409,detail="User already exists")

async def checking_password(hashed_password,password: str) -> bool:
    return pwd_context.verify(password,hashed_password)


    

async def create_access_token(data:dict,expire_date:Optional[timedelta]=None):
    to_encode = data.copy()
    if expire_date:
        expire=datetime.utcnow()+expire_date
    else:
        expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXP_MIN)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

async def create_refresh_token(data:dict):
    to_encode = data.copy()
    expire=datetime.utcnow()+timedelta(days=REFRESH_TOKEN_EXP_DAY)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

async def login(name: str,password: str,session: Session):
    user=session.exec(select(User).where(User.name == name)).first()
    if user:
        if checking_password(hashed_password=user.hashed_password,password=password):
            access_token_expire_date=timedelta(minutes=10)
            access_token=create_access_token(data={"sub":user.name},expire_date=access_token_expire_date)
            refresh_token=create_refresh_token(data={"sub":user.name})

            return {"access-token":access_token,"refresh-token":refresh_token}
        else:
            raise HTTPException(status_code=401,detail="Wrong password")
    else:
        raise HTTPException(status_code=404,detail="User not found")
    
    
async def refresh_access_token(refresh: str,session: Session):
    try:
        payload=jwt.decode(refresh,SECRET_KEY,algorithms=[ALGORITHM])
        name: str=payload.get("sub")
        if name is None:
            raise HTTPException(status_code=404,detail="Name not found")
    except jwt.ExpiredSugnatureError:
        raise HTTPException(status_code=401,detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401,detail="Invalid token")
    
    user=session.exec(select(User).where(User.name == name)).first()
    if user is None:
        raise HTTPException(status_code=404,detail="User not found")
    
    new_access_token=create_access_token(data={"sub":user.name})
    return {"access-token":new_access_token,"token-type":"Bearer"}










