from flask import Flask
from flask import g
from therm.database.db import DB

app = Flask(__name__)
app.secret_key = '\xe9}\xc6\x04\x911\xfds\x04\xce\x01\xe8\xd7\xb2\xfbw]\xc7j\x16\x99\x97dt'
DATABASE_NAME = '/home/pi/v1/therm.db'

def connect_to_database():
    return DB(DATABASE_NAME)

def get_db():
    def init():
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = connect_to_database()
        return db
    return init

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        
app.debug = True
#app.config.from_object('config')
app.get_db = get_db()

import views
import plots

