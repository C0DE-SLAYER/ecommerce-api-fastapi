import jwt
from datetime import datetime, timedelta
from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from os import getenv
from data.db import conn_db
from data.schemas import Login, LoginResp
from data.models import User
from controllers.utils.password_hashing import verify_password


LoginRouter = APIRouter()


def jwt_token(user: dict):
    payload = {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "exp": datetime.now() + timedelta(days=1, minutes=30)
    }
    access_token = jwt.encode(
        payload,
        key=getenv("SECRET_KEY"),
        algorithm=getenv("ALGORITHM")
    )
    return access_token


@LoginRouter.post("/", status_code=status.HTTP_200_OK, response_model=LoginResp)
async def login(request: Login, db: Session = Depends(conn_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if verify_password(request.password, user.password):
        token = jwt_token(user)
        context = {"token": token}
        return context
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="user credentials invalid")