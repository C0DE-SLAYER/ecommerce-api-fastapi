import jwt
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from data.db import conn_db
from os import getenv

# Environment variables or default values
SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")

security = HTTPBearer()


def get_token(credentials: HTTPAuthorizationCredentials):
    if credentials.scheme == "Bearer":
        return credentials.credentials
    return None

def verify_token(token: str):
    try:
        if token:
            # Decode the token using the secret key and algorithm
            payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Signature expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def authorize_user(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(conn_db)):
    token = get_token(credentials)
    payload = verify_token(token)
    return payload
