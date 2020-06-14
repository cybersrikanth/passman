import os
from .Form import Form
from getpass import getpass

class LoginForm(Form):
    def __init__(self):
        pass
    
    def signUp(self, User):
        userName = str(input("Enter UserName: "))
        password = str(getpass("Enter Password: "))
        repeat = str(getpass("Enter password again: "))
        if(password == repeat):
            User.name = userName
            User.password = password
            return True
        else:
            return False

    def login(self, User):
        User.name = str(input("Enter UserName: "))
        User.password = str(getpass("Enter Password: "))