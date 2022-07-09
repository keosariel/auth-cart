from app.cart.routes import _Cart, Checkout
from app import api

api.add_resource(_Cart, "/carts", "/carts/<string:public_id>")
api.add_resource(Checkout, "/carts/checkedout", "/carts/checkedout/<string:public_id>")