from sqlmodel import Session
from fastapi import APIRouter,Depends
import Services
from engine import get_session
 
router=APIRouter()

@router.post("/singup")
async def SignUp(name: str,password: str,session: Session=Depends(get_session)):
    return Services.sign_up(name,password,session)

@router.post("/login")
async def Login(name: str,password: str,session: Session=Depends(get_session)):
    return Services.login(name,password,session)

@router.post("/refreshtoken")
async def RefreshAccessToken(refresh_token,session: Session=Depends(get_session)):
    return Services.refresh_access_token(refresh_token,session)


    


