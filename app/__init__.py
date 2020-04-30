from flask import Flask

from app.lib.db import DB
import config


app = Flask(__name__)
app.secret_key = config.sys['secret_key']
app.config['DEBUG'] = True

# Open the DB connection and log the event
db = DB(config.db['db_file'])

from app.views import *
