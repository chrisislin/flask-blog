from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import sqlite3


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def validate_email(self, email):
        conn = sqlite3.connect('database.db')
        curs = conn.cursor()
        curs.execute("SELECT email FROM users where email = (?)", [email.data])
        valid_email = curs.fetchone()
        if valid_email is None:
            raise ValidationError('This Email ID is not registered. Please register before login')
