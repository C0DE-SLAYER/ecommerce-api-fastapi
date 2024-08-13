from fastapi import APIRouter, Depends, HTTPException
from data.schemas import OrderSchema
from sqlalchemy.orm import Session
from data.models import Order
from data.db import conn_db
from controllers.auth.jwtauth import authorize_user

OrderRouter = APIRouter()

@OrderRouter.post('/', response_model=OrderSchema)
def create_order(request: OrderSchema, db: Session = Depends(conn_db), payload = Depends(authorize_user)):
    try:
        new_order = Order(**request.model_dump())
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        return new_order
    except:
        raise HTTPException(status_code=400, detail='Failed to create order')
    
@OrderRouter.get('/{order_id}')
def get_order_detail(order_id: int, db: Session = Depends(conn_db), payload = Depends(authorize_user)):
    try:
        return db.query(Order).filter(Order.order_id == order_id).first()
    except:
        raise HTTPException(status_code=400, detail='Error while fetching the records')

@OrderRouter.get('/{user_id}')
def get_user_detail(user_id: int, db: Session = Depends(conn_db), payload = Depends(authorize_user)):
    try:
        return db.query(Order).filter(Order.user_id == user_id).all()
    except:
        raise HTTPException(status_code=400, detail='Error while fetching the records')
    
