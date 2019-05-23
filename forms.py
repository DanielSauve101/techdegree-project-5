from flask_wtf import Form
from wtforms import StringField, TextAreaField, IntegerField, DateField
from wtforms.validators import DataRequired


class NewEntryForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    date = DateField('Date')
    time = IntegerField('Time', validators=[DataRequired()])
    learned = StringField('Learned', validators=[DataRequired()])
    resources = StringField('Resources')
