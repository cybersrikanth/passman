from views import LoginForm
from time import sleep
from model import User
from DB import DB
from modules.Mixer import Mixer
from .PasswordController import PasswordController

class UserController:
    def __init__(self):
        self.loginForm = LoginForm()
        self.db = DB()
        self.db.connect()
        self.mixer = Mixer()
        self.User = User()
        self.PasswordController = PasswordController()

    def signUp(self):
        self.loginForm.refreshScreen()
        self.loginForm.printCenter("> SignUp <","=")
        self.loginForm.passLines(2)
        credentials = self.loginForm.signUp(self.User)
        self.loginForm.refreshScreen()
        if(credentials):
            self.User.password = self.mixer.mix(self.User.password)
            result = self.db.query("Insert into user (name, password) values (?, ?)",(self.User.name, self.User.password))
            if result['status']:
                print("user created")
            else:
                print(result["message"])

        else:
            loop = True
            print("password not match")
            while loop:
                loop = False
                choice = input("Type 'R' to retry, 'L' to goto login page : ")
                if choice.lower() == 'r':
                    self.signUp()
                elif choice.lower() =='l':
                    self.login()
                else:
                    loop = True
                    self.loginForm.clearLines(2)

        sleep(1)

    def login(self):
        self.loginForm.refreshScreen()
        self.loginForm.printCenter("> Login <","=")
        self.loginForm.passLines(2)
        self.loginForm.login(self.User)
        result = self.db.query("select * from User where name=?",(self.User.name,))
        if not len(result['rows']):
            print("invalid user")
            sleep(1)
            # self.loginForm.refreshScreen()
            return False
        hashedPassword = result['rows'][0][2]
        if self.mixer.verify(self.User.password,hashedPassword):
            self.User.isAuthenticated = True
            self.User.id = result['rows'][0][0]
            print("login successful")
            sleep(1)
            return True
        else:
            self.User.isAuthenticated = False
            print("wrong password")
            sleep(1)
            return False
        # self.loginForm.refreshScreen()
        # self.PasswordController.

    def home(self):
        available_options = ("Login", "SignUp")
        self.loginForm.refreshScreen()
        x = int(self.loginForm.columns-7)//2
        self.loginForm.printCenter("Welcome","#%")
        self.loginForm.passLines(2)
        print("Options :")
        print("=========")
        self.loginForm.passLines(1)
        for index, option in enumerate(available_options):
            print(index+1, "=>", option)
        self.loginForm.passLines(1)
        try:
            choice = int(input("Enter your choice : "))
            if choice == 1:
                if self.login():
                    self.PasswordController.home(self.User)
            elif choice == 2:
                self.signUp()
            else:
                self.home()
        except KeyboardInterrupt:
            self.loginForm.clearScreen()
            exit()
        # except:
        #     self.home()
        
        
