import os
basedir = op.path.abspath(os)

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or  'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
