#!/usr/bin/python3
import models
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from flask_login import UserMixin

Base = declarative_base()

class User(Base):
    """
        class maps out a table in the mysql database creating an object
        representation
    """
    __tablename__='January'
    id = Column(Integer, primary_key=True)
    user_ID = Column(String(255), ForeignKey('user_info.id'))
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
    schedules = relationship('User', backref='User', lazy='dynamic') 
   
    
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
