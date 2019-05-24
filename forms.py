from flask_wtf import Form
from wtforms import StringField, TextAreaField, IntegerField, DateField
from wtforms.validators import DataRequired, InputRequired


class NewEntryForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    date = DateField('Date', validators=[InputRequired()])
    time = IntegerField('Time Spent', validators=[DataRequired()])
    learned = TextAreaField('What I Learned', validators=[DataRequired()])
    resources = TextAreaField('Resources To Remember')
