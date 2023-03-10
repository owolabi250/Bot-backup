#!/usr/bin/python3
import models
import json
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from flask_login import UserMixin

Base = declarative_base()

class User(Base):
    """
        class maps out a table in the mysql database creating an object
        representation
    """
    __tablename__='January'
    id = Column(Integer, primary_key=True)
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

    def __is_serializable(self, obj_v):
        """
            private: checks if object is serializable
        """
        try:
            obj_to_str = json.dumps(obj_v)
            return obj_to_str is not None and isinstance(obj_to_str, str)
        except:
            return False

    def to_json(self):
        try:
            bm_dict = {
                    k: v if self.__is_serializable(v) else str(v)
                    for k, v in self.__dict__.items()
                    }
            bm_dict.pop('_sa_instance_state', None)
            return(bm_dict)
        except:
            return False



class user_id(Base, UserMixin):
    """
        creates a class representation of the user info 
    """
    __tablename__='User_info'
    id = Column(Integer, primary_key=True)
    User_name = Column(String(100))
    Email = Column(String(100))
    Password = Column(String(300))
    Created_at = Column(DateTime, default=datetime.utcnow)
    Updated_at = Column(DateTime)
    
    def __str__(self):
        """
            returns string representation of class objects
        """
        return f"id : {self.id}, username: {self.User_name} email: {self.Email}"

    def is_active(self):
        return True 
