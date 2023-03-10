#!/usr/bin/python3

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, BooleanField
from wtforms.validators import Email, DataRequired, Length, EqualTo, ValidationError
import models
from models.baseModel import user_id

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(),
                                        Length(min=2, max=20)])

    email = StringField("Email", validators=[DataRequired(), Email()])

    password = PasswordField("Password", validators=[DataRequired()])

    confirm_password = PasswordField("Confirm password",
                            validators= [DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign up')

    def validate_username(self, username):
        data = models.storage.access(username.data, 'User_name', user_id)
        if data:
            raise ValidationError('Username already taken')

    def validate_email(self, email):
        data = models.storage.access(email.data, 'Email', user_id)
        if data:
            raise ValidationError('Email already taken')



class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField('Login')



