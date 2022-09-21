from flask import (
	request,
	current_app
)
from flask_restful import Resource
from app.utils.functions import JSONResponse
from app.utils.decorators import args_check, login_required
from app.validators import CartItemValidator
from app.models import Cart, CartItem
from app.error_codes import E101, E102, E103, E105

class _Cart(Resource):
    
    def get(self, public_id):	
        cart = None
        
        cart = Cart.query.filter_by(public_id=public_id).first()
        if cart:
            if not cart.deleted:
                return JSONResponse(cart.to_dict())

        return JSONResponse(None, code=None, status=404)
            
    @login_required()
    def post(self, current_user):	
        cart = None
        
        cart = Cart(current_user.id)
        cart.save()
        return JSONResponse(cart.to_dict())
            
    @login_required()
    @args_check(CartItemValidator())
    def put(self, json_data, public_id, current_user):	
        cart = Cart.query.filter_by(public_id=public_id).first()
        
        if cart:
            item = CartItem(json_data.item_id, cart.id)
            item.save()
            return JSONResponse(item.to_dict())
        else:
            return JSONResponse(None, code=None, status=404)
    
    @login_required()
    @args_check(CartItemValidator())
    def delete(self, json_data, public_id, current_user):	
        cart = Cart.query.filter_by(public_id=public_id).first()
        
        if cart:
            cart.delete_item(json_data.item_id)
            cart.save()
            return JSONResponse(cart.to_dict(), code=None, status=201)
        else:
            return JSONResponse(None, code=None, status=404)


class Checkout(Resource):
    
    @login_required()
    def get(self, current_user):	
        carts = Cart.query.filter_by(user_id=current_user.id, checkedout=True).all()
        return JSONResponse(carts)
            
    @login_required()
    def post(self, public_id, current_user):	
        cart = Cart.query.filter_by(public_id=public_id).first()
        if cart.user_id == current_user.id:
            cart.checkedout = True
            return JSONResponse(cart.to_dict())
        
        return JSONResponse(None, code=E105, status=406)