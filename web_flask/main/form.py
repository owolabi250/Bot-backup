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
        data = models.storage.view(user_id)
        for k, v in data.items():
            if data[k].User_name in username:
                raise ValidationError('Username already taken')

    def validate_email(self, email):
        user = models.storage.view(user_id)
        for k, v in user.items():
            if user[k].Email in email:
                raise ValidationError('Email already taken')



class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField('Login')



