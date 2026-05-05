# Configution file
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQL_ALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db') 
    