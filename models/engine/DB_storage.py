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

    def view(self, arg=None):

        if arg is None:
            table = User
        else:
            table = user_id

        my_dict = {}
        objs = self.__session.query(table).all()
        for task in objs:
            key = task.id
            my_dict[key] = task
        return (my_dict)

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



