from fastapi import APIRouter, Depends, HTTPException
from data.schemas import CartSchema, CartUpdateSchema
from sqlalchemy.orm import Session
from data.db import conn_db
from data.models import Cart
from controllers.auth.jwtauth import authorize_user

CartRouter = APIRouter()


@CartRouter.post("/", response_model=CartSchema)
def create_shopping_cart(
    request: CartSchema, db: Session = Depends(conn_db), payload=Depends(authorize_user)
):
    try:
        new_cart = Cart(
            user_id=request.user_id,
            product_id=request.product_id,
            quantity=request.quantity,
        )
        db.add(new_cart)
        db.commit()
        db.refresh(new_cart)
        return new_cart
    except:
        raise HTTPException(
            status_code=400, detail="Error while creating shopping cart"
        )


@CartRouter.get("/{cart_id}", response_model=CartSchema)
def get_cart(
    cart_id: int, db: Session = Depends(conn_db), payload=Depends(authorize_user)
):
    try:
        cart = db.query(Cart).filter(Cart.cart_id == cart_id).first()
        return cart
    except:
        raise HTTPException(status_code=400, detail="Cart not found")


@CartRouter.put("/{cart_id}", response_model=CartUpdateSchema)
def update_cart(
    cart_id: int,
    request: CartUpdateSchema,
    db: Session = Depends(conn_db),
    payload=Depends(authorize_user),
):
    cart = db.query(Cart).filter(Cart.cart_id == cart_id).first()

    if cart:
        cart.quantity = (
            request.quantity if request.quantity is not None else cart.quantity
        )
        db.commit()
        db.refresh(cart)
        return cart

    raise HTTPException(status_code=403, detail=f"cart {cart_id} doesn't exist")


@CartRouter.delete("/{cart_id}")
def delete_cart(
    cart_id: int, db: Session = Depends(conn_db), payload=Depends(authorize_user)
):
    cart = db.query(Cart).filter(Cart.cart_id == cart_id)

    if cart.first():
        cart.delete()
        db.commit()
        return {"message": "Cart deleted successfully"}

    raise HTTPException(status_code=404, detail="Unable to locate cart")
