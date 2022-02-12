from app.cart.routes import _Cart
from app import api

api.add_resource(_Cart, "/carts", "/carts/<string:public_id>")
