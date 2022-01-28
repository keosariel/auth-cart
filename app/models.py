from app         import db, bcrypt, login_manager
from datetime    import datetime, timedelta
from flask_login import UserMixin
from hashlib import md5

import json

def get_public_id(unique_id):
    return md5(str(unique_id).encode("UTF-8")).hexdigest()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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

    def __init__(self, firstname, lastname, username, email, password):
        self.firstname = firstname
        self.lastname  = lastname
        self.username  = username
        self.email     = email
        self.set_password(password)
        
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode()
        
    def password_is_valid(self, password):
        """
        Checks the password against it's hash to validates the user's password
        """
        return bcrypt.check_password_hash(self.password, password)
    
    def set_public_id(self):
        self.public_id = get_public_id("user_"+str(self.id))
        self.save()
        
    def save(self):
        db.session.add(self)
        db.session.commit()


class Cart(db.Model):
    __tablename__  = 'cart'

    id             = db.Column(db.Integer, primary_key=True)
    public_id      = db.Column(db.Text, nullable=True)
    
    deleted        = db.Column(db.Boolean, default=False)

    created_at     = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified_at    = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    
    user_id       = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    items   = db.relationship('CartItem', order_by='CartItem.id', backref='cart', lazy=True)

    def __init__(self, user_id):
        self.user_id  = user_id
        
    def set_public_id(self):
        self.public_id = get_public_id("cart_"+str(self.id))
        self.save()
        
    def to_dict(self):
        return {
            "id": self.public_id,
            "count": len(self.items),
            "items": [ i.to_dict() for i in self.items ],
            "created": self.created_at
        }
        
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
        
    def get_misc(self):
        return json.loads(self.misc)
    
    def set_public_id(self):
        self.public_id = get_public_id("cartitem_"+str(self.id))
        self.save()
        
    def to_dict(self):
        return {
            "id": self.id,
            "unique_id": self.unique_id,
            "cart_id": self.cart.id,
            "added": self.created_at
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

