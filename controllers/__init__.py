from .auth.login import LoginRouter
from .auth.signup import SignupRouter
from .user.user import GetCurrentUserRouter
from .products.products import ProductsRouter
from .category.category import CategoryRouter
from .cart.cart import CartRouter
from .order.order import OrderRouter
from .payment.payment import PaymentRouter

def include_router(app):
    app.include_router(LoginRouter, prefix='/login', tags=["Login"])
    app.include_router(SignupRouter, prefix='/signup', tags=["Signup"])
    app.include_router(GetCurrentUserRouter, prefix='/user', tags=["User"])
    app.include_router(ProductsRouter, prefix='/product', tags=["Products"])
    app.include_router(CategoryRouter, prefix='/category', tags=["Category"])
    app.include_router(CartRouter, prefix='/cart', tags=["Cart"])
    app.include_router(OrderRouter, prefix='/order', tags=["Order"])
    app.include_router(PaymentRouter, prefix='/payment', tags=["Payment"])
