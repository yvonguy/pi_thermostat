from flask import Flask
from therm.database.db import DB

app = Flask(__name__)
app.config.from_object('config')
app.db = DB('therm.db')

from therm.app import views
from therm.app import plots

