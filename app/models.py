from app         import db, bcrypt
from datetime    import datetime, timedelta
from flask_login import UserMixin
from hashlib import md5
from flask import current_app
import uuid
import jwt

import json

def get_public_id(unique_id):
    return md5(str(unique_id).encode("UTF-8")).hexdigest()

class User(db.Model, UserMixin):
    __tablename__  = 'user'

    id             = db.Column(db.Integer, primary_key=True)
    public_id      = db.Column(db.Text, nullable=True)
    firstname      = db.Column(db.String(30), nullable=True)
    lastname       = db.Column(db.String(30), nullable=True)
    username       = db.Column(db.String(256), nullable=True)
    email          = db.Column(db.String(256), nullable=False)
    password       = db.Column(db.String(256), nullable=False)
    
    deleted        = db.Column(db.Boolean, default=False)

    created_at     = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified_at    = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    
    carts   = db.relationship('Cart', order_by='Cart.id', backref='user', lazy=True)

    def __init__(self, firstname, lastname, username, email):
        self.firstname = firstname
        self.lastname  = lastname
        self.username  = username
        self.email     = email
        self.public_id = str(uuid.uuid4())
        
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode()
        
    def password_is_valid(self, password):
        """
        Checks the password against it's hash to validates the user's password
        """
        return bcrypt.check_password_hash(self.password, password)
    
    def to_dict(self):
        return {
            "id": self.public_id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "username": self.username,
            "email": self.email
        }
        
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def generate_token(self):
        """Generates the access token"""

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(hours=672),
                'iat': datetime.utcnow(),
                'sub': self.id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )

            if type(jwt_string) == bytes:
                jwt_string = jwt_string.decode()

            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithms=['HS256'])
            return True, payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return False, "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return False, "Invalid token. Please register or login"

        return False, "Invalid token. Please register or login"



class Cart(db.Model):
    __tablename__  = 'cart'

    id             = db.Column(db.Integer, primary_key=True)
    public_id      = db.Column(db.Text, nullable=True)
    
    deleted        = db.Column(db.Boolean, default=False)

    checkedout     = db.Column(db.Boolean, default=False)

    created_at     = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified_at    = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    
    user_id       = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    items   = db.relationship('CartItem', order_by='CartItem.id', backref='cart', lazy=True)

    def __init__(self, user_id):
        self.user_id  = user_id
        self.public_id = str(uuid.uuid4())
        
    def to_dict(self):
        items = [i for i in self.items if not i.deleted]
        return {
            "id": self.public_id,
            "count": len(items),
            "items": [ i.to_dict() for i in items ]
        }
    
    def delete_item(self, item_id):
        items = [i for i in self.items if not i.deleted]

        for i in items:
            if i.unique_id == item_id:
                i.deleted = True
                i.save()
                return True 
    def save(self):
        db.session.add(self)
        db.session.commit()


class CartItem(db.Model):
    __tablename__  = 'cart_item'

    id             = db.Column(db.Integer, primary_key=True)
    public_id      = db.Column(db.Text, nullable=True)
    unique_id      = db.Column(db.Text, nullable=False)
    
    misc           = db.Column(db.Text, nullable=False)
    cart_id        = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    
    deleted        = db.Column(db.Boolean, default=False)

    created_at     = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified_at    = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, unique_id, cart_id,misc="{}"):
        self.unique_id  = unique_id
        self.cart_id    = cart_id
        self.misc = json.dumps(misc)
        self.public_id = str(uuid.uuid4())
        
    def get_misc(self):
        return json.loads(self.misc)
    
    def to_dict(self):
        if not self.deleted:
            return {
                "id": self.public_id,
                "unique_id": self.unique_id,
                "cart_id": self.cart.public_id
            }
        
        return {}
    def delete(self):
        self.deleted = True
        self.save()

    def save(self):
        db.session.add(self)
        db.session.commit()

