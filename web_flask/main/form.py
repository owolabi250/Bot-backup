#!/usr/bin/python3

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, BooleanField
from wtforms.validators import Email, DataRequired, Length, EqualTo, ValidationError
import models
from .validation import is_valid
from models.baseModel import user_id

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(),
                                        Length(min=2, max=20)])

    email = StringField("Email", validators=[DataRequired(), Email()])

    password = PasswordField("Password", validators=[DataRequired(),
                                                     Length(min=8)])

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
        if email.data == '' and len(email.data) < 4:
            raise ValidationError('Email must be at least 4 characters')
        if not is_valid(email.data):
            raise ValidationError('Invalid email')
    
    def validate_password(self, password):
        if len(password.data) < 8:
            raise ValidationError('Password must be at least 8 characters')
        if not any(char.isdigit() for char in password.data):
            raise ValidationError('Password must contain at least 1 number')



class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField('Login')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = models.storage.access(email.data, 'Email', user_id)
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')
        if not is_valid(email.data):
            raise ValidationError('Invalid email')

class ResetPasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
    def validate_password(self, password):
        if len(password.data) < 8:
            raise ValidationError('Password must be at least 8 characters')
        if not any(char.isdigit() for char in password.data):
            raise ValidationError('Password must contain at least 1 number')




