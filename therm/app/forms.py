from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class ThermometerRenameForm(Form):
    name = StringField('name', validators=[DataRequired()])
    
