from modules.CheckEnv import CheckEnv
from modules.PassGen import PassGen
from DB import DB
from views import LoginForm
from controller import UserController
from time import sleep

# env = CheckEnv()
# env.check()
refresh = 0
while True:
    try:
        login = LoginForm()
        if refresh:
            login.refreshScreen()
        else:
            login.allocateScreen()
        refresh += 1
        # login.signUp()
        # sleep(5)
        auth = UserController()
        # auth.newUser()
        auth.home()

        db = DB()
        db.connect()
        # db.query("Insert into user (name, password) values ('srikanth', 'password')")
        db.close()
    except KeyboardInterrupt:
        login.clearScreen()
