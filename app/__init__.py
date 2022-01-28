from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_bcrypt import Bcrypt
from app.config import Config


app = Flask(__name__)
app.config.from_object(Config)     # adding Config

db  = SQLAlchemy(app)
api = Api(app)
bcrypt = Bcrypt(app)

from app.models import *