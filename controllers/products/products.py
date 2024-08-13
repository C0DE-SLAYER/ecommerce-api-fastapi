from fastapi import APIRouter, Depends, HTTPException
from data.schemas import ProductSchema, ProductUpdateSchema
from data.db import conn_db
from data.models import Product
from sqlalchemy.orm import Session
from controllers.auth.jwtauth import authorize_user

ProductsRouter = APIRouter()

@ProductsRouter.post('/', response_model=ProductSchema)
def create_product(request: ProductSchema, db: Session = Depends(conn_db), payload = Depends(authorize_user)):
    try:
        new_product = Product(**request.model_dump())
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    except:
        raise HTTPException(status_code=400, detail="Failed to create product")

@ProductsRouter.get('/', response_model=list[ProductSchema])
def get_all_product(db: Session = Depends(conn_db), payload = Depends(authorize_user)):
    try:
        return db.query(Product).all()
    except:
        raise HTTPException(status_code=404, detail='error while getting products')
    

@ProductsRouter.get('/{product_id}', response_model=ProductSchema)
def get_product(product_id:int,db: Session = Depends(conn_db), payload = Depends(authorize_user)):
    try:
        return db.query(Product).filter(Product.product_id == product_id).first()
    except:
        raise HTTPException(status_code=404, detail='error while getting products')
    

@ProductsRouter.put('/{product_id}', response_model=ProductUpdateSchema)
def update_product(product_id:int, request: ProductUpdateSchema, db: Session = Depends(conn_db), payload = Depends(authorize_user)):
    try:
        product = db.query(Product).filter(Product.product_id == product_id)

        if product.first():
            product_dict = request.model_dump(exclude_unset=True)
            product_dict = {k: v for k, v in product_dict.items() if v not in ("string", 0, "", " ")}
            product.update(product_dict)
            
            db.commit()
        
        return product
    except Exception as e:
        raise HTTPException(status_code=403, detail=f'error while updating products')
    
@ProductsRouter.delete('/{product_id}')
def delete_product(product_id: int, db: Session = Depends(conn_db), payload = Depends(authorize_user)):
    product = db.query(Product).filter(Product.product_id == product_id)

    if product.first():
        product.delete()
        db.commit()
        return {'message': 'Deleted successfully'}
    
    raise HTTPException(status_code=404, detail="Failed to delete the Product")