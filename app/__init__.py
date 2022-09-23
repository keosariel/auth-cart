from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from app.config import Config


app = Flask(__name__)
app.config.from_object(Config)     # adding Config

db  = SQLAlchemy(app)
api = Api(app)
bcrypt = Bcrypt(app)
cors = CORS(app, resources={r"*": {"origins": "*"}})

@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

from app.users import *
from app.cart import *
from app.models import *

def create_db():
    db.create_all()