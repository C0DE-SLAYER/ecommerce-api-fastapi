from fastapi import APIRouter, status, HTTPException, Depends
from data.db import session_local
from sqlalchemy.orm import Session
from data.db import conn_db
from controllers.auth.jwtauth import authorize_user
from data.models import User


GetCurrentUserRouter = APIRouter()
db = session_local()

@GetCurrentUserRouter.get("/me/", status_code=status.HTTP_200_OK)
async def get_current_user(db: Session = Depends(conn_db), payload=Depends(authorize_user)):
    try:
        user = db.query(User).filter(User.id == payload['user_id']).first()
        return user
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Bad request')
