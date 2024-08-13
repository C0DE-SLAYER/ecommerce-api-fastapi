from fastapi import APIRouter, status, HTTPException
from data.db import session_local
from data.schemas import SignUpSchema
from data.models import User
from controllers.utils.password_hashing import get_password_hash


SignupRouter = APIRouter()
db = session_local()

@SignupRouter.post("/", response_model=SignUpSchema, status_code=status.HTTP_201_CREATED)
def sign_up(request: SignUpSchema):

    user_email = db.query(User).filter(User.email == request.email).first()

    if user_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
                    name=request.name, 
                    email=request.email, 
                    password=get_password_hash(request.password)
                )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
