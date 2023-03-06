#!/usr/bin/python3
from models.baseModel import user_id
import hashlib
import models
import getpass
arg = user_id

class Login(arg):
    """
        class creates a login system interface for the commandline
        by mapping out an instance of the user_id class
    """
    def __init__(self):
        self.__data = models.storage.view(arg)


    def login(self):
        """
            class method enables access to the commandline interface
            if provided userinfo matches that of those queried from database
        """
        user_n = str(input("username: "))
        key = getpass
        pass_k = str(key.getpass())
        pass_code = self.__data[1].Password
        username = self.__data[1].User_name
        chance = 3
        while chance != 0:
            p = pass_k.encode()
            passphrase = hashlib.sha256(p).hexdigest()
            if user_n == username and passphrase == pass_code:
                print(">>> Login Successful")
                return True
            else:
                print("Incorrect Username and Password try again")
                chance -= 1
                if chance == 1:
                    print("\n>>> warning last attempt!!!\n")
                elif chance == 0:
                    print("\n>>>Account locked <<<\n")
                    return False
            user_n = str(input("username: "))
            pass_k = str(key.getpass())
