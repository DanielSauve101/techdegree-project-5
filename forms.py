from flask_wtf import Form
from wtforms import (StringField, TextAreaField, IntegerField, DateField,
                     PasswordField)
from wtforms.validators import (DataRequired, Regexp, Length, EqualTo,
                                ValidationError)

from models import User


def username_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('Username already exists')


class RegisterForm(Form):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should be one word, letters, "
                         "numbers, and underscores only.")
            ),
            username_exists
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=4),
            EqualTo('password2', message='Passwords must match')
        ])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class EntryForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    time = IntegerField('Time Spent', validators=[DataRequired()])
    learned = TextAreaField('What I Learned', validators=[DataRequired()])
    resources = TextAreaField('Resources To Remember')
