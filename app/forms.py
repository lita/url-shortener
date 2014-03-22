from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required

class UrlForm(Form):
    url = TextField('url', validators = [Required()])