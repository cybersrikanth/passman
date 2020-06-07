from modules.PassGen import PassGen
from DB import DB
from views import LoginForm
from controller import UserController
from time import sleep


refresh = 0
while True:
    try:
        db = DB()
        db.connect()
        login = LoginForm()
        if refresh:
            login.refreshScreen()
        else:
            login.allocateScreen()
        refresh += 1
        auth = UserController()
        auth.home()

        db.close()
    except KeyboardInterrupt:
        login.clearScreen()
