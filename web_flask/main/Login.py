#!/usr/bin/python3
import models
from models.baseModel import user_id
from werkzeug.security import generate_password_hash, check_password_hash


class Login(user_id):
    key = None
    __data = models.storage.view(user_id)
    password_hash = __data[key].Password
    
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)




