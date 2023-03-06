#!/usr/bin/python3

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, BooleanField
from wtforms.validators import Email, DataRequired, Length, EqualTo


class RegisterForm(FlaskForm):
    username = StringField("username", validators=[DataRequired(),
                                        Length(min=2, max=20)])

    email = StringField("email", validators=[DataRequired(), Email()])

    password = PasswordField("password", validators=[DataRequired()])

    confirm_password = PasswordField("confirm password",
                            validators= [DataRequired(), EqualTo('password')])

    submit = SubmitField('sign up')



class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField('login')



