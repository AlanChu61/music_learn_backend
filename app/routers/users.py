from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta
from ..database import get_db
from ..models import User
from ..crud import get_current_user

router = APIRouter()

# 秘鑰和算法
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class LoginRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# 創建 JWT Token
# Modify Token Creation to Include Role
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/login", response_model=Token)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Email not found")
    if request.password != user.password:
        raise HTTPException(status_code=400, detail="Incorrect password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# 使用 JWT Token 獲取當前用戶資料
@router.get("/me")
def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
        "instrument": current_user.instrument,
    }
