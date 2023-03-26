#!/usr/bin/python3
import models
from datetime import datetime, timedelta
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from flask_login import UserMixin
import jwt

Base = declarative_base()

class Auto_courses:
    Days = Column(DateTime)
    Course = Column(String(50))
    Topic = Column(String(50))
    Reminder = Column(DateTime)
    Target = Column(Boolean)
    Created_at = Column(DateTime, default=datetime.utcnow)
    Updated_at = Column(DateTime)
    Average = Column(Integer)

    def __str__(self):
        """
            returns a string representation of the class 
        """
        return f"Date: {self.Days} Course: {self.Course} Topic: {self.Topic}\
                Average: {self.Average} Reminder: {self.Reminder}\
                Created: {self.Created_at}"


class User(Base, Auto_courses):
    """
        class maps out a table in the mysql database creating an object
        representation
    """
    __tablename__='January'
    id = Column(Integer, primary_key=True)
    user_ID = Column(Integer, ForeignKey('user_info.id'))


class AutoSchedule(Base, Auto_courses):
     """
         class maps out a table in the mysql database creating an object
         representation
     """
     __tablename__='PythonDB'
     id = Column(Integer, primary_key=True)
     user_ID = Column(Integer, ForeignKey('user_info.id'))


class JSCourse(Base, Auto_courses):
    __tablename__ = 'JavascriptDB'
    id = Column(Integer, primary_key=True)
    user_ID = Column(Integer, ForeignKey('user_info.id'))  


class user_id(Base, UserMixin):
    """
        creates a class representation of the user info 
    """
    __tablename__='user_info'
    id = Column(String(255), primary_key=True)
    User_name = Column(String(100))
    Email = Column(String(100))
    Password = Column(String(300))
    Created_at = Column(DateTime, default=datetime.utcnow)
    Updated_at = Column(DateTime)
    schedules = relationship('User', backref='January', lazy='dynamic')
    auto_schedules = relationship('AutoSchedule', backref='PythonDB', lazy='dynamic')
    JScourse = relationship('JSCourse', backref='JSCourse', lazy='dynamic')
   
    
    def __str__(self):
        """
            returns string representation of class objects
        """
        return f"id : {self.id}, username: {self.User_name} email: {self.Email}"

    """
        Flask-Login integration checks if a user is currently logged in
        to a session
    """
    def is_active(self):
        return True 

    def get_reset_token(self):
        from web_flask.app import app
        user = models.storage.access(self.id, 'id', user_id)
        if not user:
            raise Exception('User not found')
        token = token_payload = {'user_id': self.id, 'exp': datetime.utcnow() + timedelta(minutes=2)}
        token = jwt.encode(token_payload, app.config['SECRET_KEY'])
        return token.encode('utf-8').decode()

    @staticmethod
    def verify_reset_token(token):
        from web_flask.app import app
        try:
            token_payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            my_id = token_payload['user_id']
        except jwt.ExpiredSignatureError:
            return None
        except (jwt.InvalidTokenError, KeyError):
            return None
        user = models.storage.access(my_id, 'id', user_id)
        return user

