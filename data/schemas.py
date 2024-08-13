from pydantic import BaseModel, EmailStr, Field
from typing import Union, Optional


class SignUpSchema(BaseModel):
    name: str 
    email: EmailStr
    password: str 


class Login(BaseModel):
    email: EmailStr
    password: str

class LoginResp(BaseModel):
    token: str


class ProductSchema(BaseModel):
    # product_id: int
    product_name: str
    product_desc: str
    product_price: int
    product_stock: int
    category_id: int

class ProductUpdateSchema(BaseModel):
    product_name: Optional[str] = None
    product_desc: Optional[str] = None
    product_price: Optional[int] = None
    product_stock: Optional[int] = None
    category_id: Optional[int] = None



class CategorySchema(BaseModel):
    # category_id: int
    category_name: str

class CartSchema(BaseModel):
    # cart_id: int
    user_id: int
    product_id: int
    quantity: int

class CartUpdateSchema(BaseModel):
    quantity: int

class OrderSchema(BaseModel):
    user_id: int
    address: str
    payment_method: str
    cart_id: int

class PaymentSchema(BaseModel):
    user_id: int
    status: str
    amount: int
