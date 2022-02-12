import os

basedir = os.path.dirname(os.path.abspath(__file__))

base_dir  = os.path.split(basedir)[0]
# base_dir  = os.path.split(base_dir)[0]

class Config:
    SECRET_KEY              = "secret"
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{base_dir}/db/app.db'
    DEBUG                   =  True             # some Flask specific configs