from fastapi import APIRouter, Depends, HTTPException
from data.schemas import CategorySchema
from data.db import conn_db
from data.models import Category
from sqlalchemy.orm import Session
from controllers.auth.jwtauth import authorize_user

CategoryRouter = APIRouter()


@CategoryRouter.post("/", response_model=CategorySchema)
def create_category(
    request: CategorySchema,
    payload=Depends(authorize_user),
    db: Session = Depends(conn_db),
):
    try:
        new_category = Category(category_name=request.category_name)
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category
    except:
        raise HTTPException(status_code=400, detail="Failed to create category")


@CategoryRouter.get("/", response_model=list[CategorySchema])
def get_all_category(db: Session = Depends(conn_db), payload=Depends(authorize_user)):
    try:
        category = db.query(Category).all()
        return category
    except:
        raise HTTPException(status_code=404, detail="Failed to get category")


@CategoryRouter.put("/{category_id}", response_model=CategorySchema)
def update_category(
    category_id: int,
    request: CategorySchema,
    db: Session = Depends(conn_db),
    payload=Depends(authorize_user),
):
    category = db.query(Category).filter(Category.category_id == category_id).first()

    if category:
        category.category_name = (
            request.category_name
            if request.category_name is not None
            else category.category_name
        )
        db.commit()
        db.refresh(category)
        return category

    raise HTTPException(status_code=403, detail="Failed to update category")


@CategoryRouter.delete("/{category_id}")
def delete_category(
    category_id: int, db: Session = Depends(conn_db), payload=Depends(authorize_user)
):
    category = db.query(Category).filter(Category.category_id == category_id)

    if category.first():
        category.delete()
        db.commit()
        return {"message": "deleted successfully"}

    raise HTTPException(status_code=404, detail="Failed to delete the category")
