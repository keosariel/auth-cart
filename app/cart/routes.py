from flask import (
	request,
	current_app
)
from flask_restful import Resource
from app.utils.functions import JSONResponse
from app.utils.decorators import args_check, login_required
from app.validators import CartItemValidator
from app.models import Cart, CartItem
from app.error_codes import E101, E102, E103

class _Cart(Resource):
    
    def get(self, public_id):	
        cart = None
        
        cart = Cart.query.filter_by(public_id=public_id).first()
        
        return JSONResponse(cart.to_dict())
            
    @login_required()
    def post(self, current_user):	
        cart = None
        
        cart = Cart(current_user.id)
        cart.save()
        cart.set_public_id()
        
        return JSONResponse(cart.to_dict())
            
    @login_required()
    @args_check(CartItemValidator())
    def put(self, json_data, public_id, current_user):	
        cart = Cart.query.filter_by(public_id=public_id).first()
        
        if cart:
            item = CartItem(json_data.item_id, cart.id)
        
            return JSONResponse(item.to_dict())
        else:
            return JSONResponse(None, code=None, status=404)
