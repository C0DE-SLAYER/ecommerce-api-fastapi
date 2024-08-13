from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base


class User(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)


class Product(Base):

    __tablename__ = "product"

    product_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_name = Column(String)
    product_desc = Column(String)
    product_price = Column(Integer)
    product_stock = Column(Integer)
    category_id = Column(Integer, ForeignKey("category.category_id"), default=None)

    category = relationship("Category")


class Category(Base):

    __tablename__ = "category"

    category_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category_name = Column(String)


class Cart(Base):

    __tablename__ = "cart"

    cart_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    product_id = Column(Integer, ForeignKey("product.product_id"))
    quantity = Column(Integer)

    user = relationship("User")
    product = relationship("Product")

class Order(Base):

    __tablename__ = "order"

    order_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    address = Column(String)
    payment_method = Column(String)
    cart_id = Column(Integer, ForeignKey("cart.cart_id"))

    user = relationship("User")
    cart = relationship("Cart")


class Payment(Base):

    __tablename__ = "payment"

    payment_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    status = Column(String)
    amount = Column(Integer)
    transaction_id = Column(String)

    user = relationship("User")
