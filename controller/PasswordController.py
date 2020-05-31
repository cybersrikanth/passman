from time import sleep
from views import PasswordForm
from model import Password
from DB import DB
from modules.Locker import Locker

class PasswordController:
    def __init__(self):
        self.PasswordForm = PasswordForm()
        self.credential = Password()
        self.db = DB()
        self.db.connect()
        self.Locker = Locker()

    def greet(self):
        self.PasswordForm.printRight(" Welcome "+self.User.name+" <<<", ">")

    def insert(self):
        self.PasswordForm.refreshScreen()
        self.greet()
        self.PasswordForm.passLines(1)
        print("Insert Credential :")
        print("===================")
        self.PasswordForm.passLines(1)
        self.PasswordForm.newCredential(self.credential)
        self.decryptAll()
        key = self.User.password
        for prev_credential in self.data:
            if prev_credential.website == self.credential.website and prev_credential.username == self.credential.username:
                print("user account already exist, do you like to update?")
                choice = input("type 'yes' to update password : ")
                if choice.lower() == "yes":
                    self.PasswordForm.clearLines(3)
                    self.credential.password = self.Locker.encrypt(self.credential.password, key)
                    result = self.db.query("update Password set password = ? where id = ? and user = ?",(self.credential.password, prev_credential.id, self.User.id))
                    if result['status']:
                        print("updated..")
                    else:
                        print(result["message"])
                else:
                    self.PasswordForm.clearLines(3)
                    print("skipped...")
                sleep(2)
                return

        self.credential.password = self.Locker.encrypt(self.credential.password, key)
        self.credential.website = self.Locker.encrypt(self.credential.website,key)
        self.credential.username = self.Locker.encrypt(self.credential.username, key)
        result = self.db.query("Insert into Password (user, website, username, password) values (?, ?, ?, ?)",(self.User.id, self.credential.website, self.credential.username, self.credential.password))
        if result['status']:
            print("inserted")
        else:
            print(result["message"])
        sleep(2)

    def view(self):
        self.decryptAll()
        n = self.PasswordForm.lines - 10
        websites = tuple(set(map(lambda credential: credential.website, self.data)))
        chunked = [websites[i * n:(i + 1) * n] for i in range((len(websites) + n - 1) // n )]
        page = 0
        while True:
            self.PasswordForm.refreshScreen()
            self.greet()
            self.PasswordForm.passLines(1)
            print("View Credential :")
            print("===================")
            self.PasswordForm.passLines(1)
            for index, value in enumerate(chunked[page]):
                print((n*page)+index+1,"=>",value)
            self.PasswordForm.passLines(2)
            choice = input("next = 'N/n' |  prev = 'P/p' | back ='B/b' :")
            if choice.isdigit() and len(websites)>=int(choice) and int(choice)>0:
                choice = int(choice)
                website = websites[choice-1]
                selected_credentials = tuple(filter(lambda credential: credential.website==website , self.data))
                user_names = tuple(map(lambda credential: credential.username, selected_credentials))
                chunked_names = [user_names[i * n:(i + 1) * n] for i in range((len(user_names) + n - 1) // n )]
                page1 = 0
                while True:
                    self.PasswordForm.refreshScreen()
                    self.greet()
                    self.PasswordForm.passLines(1)
                    print("View Credential :")
                    print("===================")
                    self.PasswordForm.printCenter("> | "+website+" | <","=")
                    self.PasswordForm.passLines(1)
                    for index, value in enumerate(chunked_names[page]):
                        print((n*page)+index+1,"=>",value)
                    self.PasswordForm.passLines(2)
                    choice1 = input("next = 'N/n' |  prev = 'P/p' | back ='B/b' :")
                    if choice1.isdigit() and len(user_names)>=int(choice1) and int(choice1)>0:
                        choice1 = int(choice1)
                        self.PasswordForm.refreshScreen()
                        self.greet()
                        self.PasswordForm.passLines(1)
                        print("View Credential :")
                        print("===================")
                        self.PasswordForm.printCenter("> | "+website+" | <","=")
                        self.PasswordForm.passLines(1)
                        print("UserName = ", selected_credentials[choice1-1].username)
                        print("Password = ", selected_credentials[choice1-1].password)
                        self.PasswordForm.passLines(2)
                        for i in range(30,0):
                            self.PasswordForm.printRight(str(i)+" seconds---","-")
                            sleep(1)
                            self.PasswordForm.clearLines(2)
                    elif choice1.lower()=="n" and len(chunked_names)>page1+1:
                        page1 += 1
                    elif choice1.lower()=="p" and page1>0:
                        page1 -= 1
                    elif choice1.lower() == "b":
                        break
                    else:
                        self.PasswordForm.clearLines(2)
            elif choice.lower()=="n" and len(chunked)>page+1:
                page += 1
            elif choice.lower()=="p" and page>0:
                page -= 1
            elif choice.lower() == "b":
                break
            else:
                self.PasswordForm.clearLines(2)

        # for i in self.data:
        #     print(i.username)
        # sleep(10)

    def delete(self):
        pass

    def decryptAll(self):
        self.data = []
        key = self.User.password
        result = self.db.query("select * from Password where user=? ",(self.User.id,))
        for row in result['rows']:
            credential = Password()
            credential.id = row[0]
            credential.website = self.Locker.decrypt(row[2],key)
            credential.username = self.Locker.decrypt(row[3],key)
            credential.password = self.Locker.decrypt(row[4],key)
            self.data.append(credential)


    def home(self, User):
        self.User = User
        available_options = ("insert credential", "view credential", "delete credential")
        while True:
            self.PasswordForm.refreshScreen()
            self.PasswordForm.printCenter("> Home <", "=")
            # self.PasswordForm.printRight(" Welcome "+User.name+" <<<", ">")
            self.greet()
            self.PasswordForm.passLines(1)
            print("Options :")
            print("=========")
            self.PasswordForm.passLines(1)
            for index, option in enumerate(available_options):
                print(index+1, "=>", option)
            self.PasswordForm.passLines(1)
            try:
                choice = int(input("Enter your choice : "))
                if choice == 1:
                    if self.insert():
                        self.PasswordController.home(self.credential)
                elif choice == 2:
                    self.view()
                else:
                    self.home()
            except KeyboardInterrupt:
                self.PasswordForm.clearScreen()
                exit()