from fastapi import APIRouter, Depends, HTTPException
from data.schemas import PaymentSchema
from sqlalchemy.orm import Session
from data.db import conn_db
from data.models import Payment
from controllers.auth.jwtauth import authorize_user
from uuid import uuid4

PaymentRouter = APIRouter()


@PaymentRouter.post("/", response_model=PaymentSchema)
def create_payment(
    request: PaymentSchema,
    db: Session = Depends(conn_db),
    payload=Depends(authorize_user),
):
    try:
        new_payment = Payment(
            user_id=request.user_id,
            status=request.status,
            amount=request.amount,
            transaction_id=uuid4()
        )
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)
        return new_payment
    except Exception as e:
        raise HTTPException(
            status_code=400, detail="Error while creating shopping cart"
        )
