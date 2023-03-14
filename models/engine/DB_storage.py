#!/usr/bin/python3
import sqlalchemy
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.baseModel import User, Base, user_id 


class DBstorage:
    __engine = None
    __session = None
    """
        The __init__ method is used to create a connection to the database
    """
    def __init__(self):
        Mysql_User = os.getenv('MYSQL_USR')
        Mysql_Host = os.getenv('MYSQL_HOST')
        Mysql_Pass = os.getenv('MYSQL_PASS')
        Mysql_Db = os.getenv('MYSQL_DB')
        port = os.getenv('PORT')
        self.__engine = create_engine('mysql://{}:{}@{}:{}/{}'.
                                                 format(Mysql_User,
                                                        Mysql_Pass,
                                                        Mysql_Host,
                                                        port,
                                                        Mysql_Db))
    """
       The View method is used to get the user data from the database
       it takes in the user_id as an argument and returns a dictionary
       of all user items in the database
    """

    def view(self, my_id):
        table = user_id
        my_dict = {}
        tasks = {}
        objs = self.__session.query(table).all()

        for task in objs:
            key = task.id
            my_dict[key] = task

        data = my_dict.get(my_id)
        file = data.schedules
        for items in file:
            tasks[items.id] = {
                    "Date" : items.Days,
                    "Course" : items.Course,
                    "Topic" : items.Topic,
                    "Reminder" : items.Reminder,
                    "Target" : items.Target,
                    "Average" : items.Average,
                    "Created_at" : items.Created_at,
                    "Updated_at" : items.Updated_at
                }
        return my_dict, tasks

    """
        access method gets the users identity saved in the database
        it takes in the user_id in the obj var, the key to specify an info and
        the user_id class as an argument and returns a dictionary of the user
    """
    def access(self, obj, key, arg):
        index = {'Email': user_id.Email,
                 'Password' : user_id.Password,
                 'User_name' : user_id.User_name,
                 'id' : user_id.id
                }
        query = self.__session.query(arg)
        data = query.filter(index[key] == obj).first()
        return data

    def new(self, obj):
        """
            add the object to the current database session
        """
        self.__session.add(obj) 
    
    def save(self):
        """
            commit all changes of the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
            delete from the current database session obj if not None
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
            reloads data from the database
        """
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """
            call remove() method on the private session attribute
        """
        self.__session.remove()



