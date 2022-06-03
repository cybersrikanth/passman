from time import sleep
from views import PasswordForm
from model import Password
from DB import DB
from modules.Locker import Locker
from modules.Loaders import DotLoader
import cursor

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
        try:
            self.PasswordForm.refreshScreen()
            self.greet()
            self.PasswordForm.passLines(1)
            print("Insert Credential :")
            print("===================")
            self.PasswordForm.passLines(1)
            self.PasswordForm.newCredential(self.credential)
            self.decryptAll("synchronizing...")
            key = self.User.password
            temp = self.credential.password
            for prev_credential in self.data:
                try:
                    pass
                except KeyboardInterrupt:
                    break
                if prev_credential.website == self.credential.website and prev_credential.username == self.credential.username:
                    print("user account already exist, do you like to update?")
                    choice = input("type 'yes' to update password : ")
                    if choice.lower() == "yes":
                        self.PasswordForm.clearLines(3)
                        self.credential.password = self.Locker.encrypt(self.credential.password, key)
                        result = self.db.query("update Password set password = ? where id = ? and user = ?",(self.credential.password, prev_credential.id, self.User.id))
                        if result['status']:
                            print("credential updated")
                            print("updated password :",self.PasswordForm.retRed(temp))
                            for i in range(15, 0, -1):
                                sleep(1)
                                self.PasswordForm.printRight(str(i)+" seconds---","-")
                                self.PasswordForm.clearLines(2)
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
                print("credential saved")
                print("Generated password :",self.PasswordForm.retRed(temp))
                for i in range(15, 0, -1):
                    sleep(1)
                    self.PasswordForm.printRight(str(i)+" seconds---","-")
                    self.PasswordForm.clearLines(2)
            else:
                print(result["message"])
                sleep(2)
        except:
            pass
        

    def view(self):
        try:
            self.decryptAll()
            n = self.PasswordForm.lines - 10
            websites = sorted(tuple(set(map(lambda credential: credential.website, self.data))))
            chunked = [websites[i * n:(i + 1) * n] for i in range((len(websites) + n - 1) // n )]
            page = 0
            while True:
                self.PasswordForm.refreshScreen()
                self.greet()
                self.PasswordForm.passLines(1)
                print("View Credential :")
                print("===================")
                self.PasswordForm.passLines(1)
                if len(chunked)==0:
                    print("No credentials found..")
                    sleep(2)
                    return
                for index, value in enumerate(chunked[page]):
                    print((n*page)+index+1,"=>",value)
                self.PasswordForm.passLines(2)
                choice = input("next = 'N/n' |  prev = 'P/p' | back ='B/b' :")
                if choice.isdigit() and len(websites)>=int(choice) and int(choice)>0:
                    choice = int(choice)
                    website = websites[choice-1]
                    selected_credentials = sorted(tuple(filter(lambda credential: credential.website==website , self.data)),key=lambda x: x.username)
                    user_names = sorted(tuple(map(lambda credential: credential.username, selected_credentials)))
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
                        for index, value in enumerate(chunked_names[page1]):
                            print((n*page1)+index+1,"=>",value)
                        self.PasswordForm.passLines(2)
                        choice1 = input("next = 'N/n' |  prev = 'P/p' | back ='B/b' | delete ='D/d-index' :")
                        if choice1.isdigit() and len(user_names)>=int(choice1) and int(choice1)>0:
                            choice1 = int(choice1)
                            self.PasswordForm.refreshScreen()
                            self.greet()
                            self.PasswordForm.passLines(1)
                            print("View Credential :")
                            self.PasswordForm.passLines(1)
                            self.PasswordForm.printCenter("> | "+website+" | <","=")
                            self.PasswordForm.passLines(1)
                            print("UserName = ", selected_credentials[choice1-1].username)
                            print("Password = ", selected_credentials[choice1-1].password)
                            self.PasswordForm.passLines(2)
                            try:
                                cursor.hide()
                                for i in range(30, 0, -1):
                                    self.PasswordForm.printRight(str(i)+" seconds---","-")
                                    sleep(1)
                                    self.PasswordForm.clearLines(2)
                            except KeyboardInterrupt:
                                cursor.show()
                                break
                        elif choice1.lower()=="n" and len(chunked_names)>page1+1:
                            page1 += 1
                        elif choice1.lower()=="p" and page1>0:
                            page1 -= 1
                        elif choice1.lower() == "b":
                            break
                        elif len(choice1)>1 and choice1.lower()[0] == "d" and len(choice1.split("-"))==2 and choice1.split("-")[1].isdigit() and 0<int(choice1.split("-")[1])<=len(selected_credentials):
                            confirm = input("Type 'CONFIRM' to delete credential : ")
                            if confirm == "CONFIRM":
                                self.delete(selected_credentials[int(choice1.split("-")[1])-1])
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
        except:
            pass
        


    def delete(self, credential):
        result = self.db.query("delete from Password where id = ? and user = ?",(credential.id, self.User.id))
        if result['status']:
            print("credential deleted ...")
        else:
            print(result["message"])
        self.decryptAll("synchronizing...")

    def deleteUser(self):
        self.PasswordForm.refreshScreen()
        self.greet()
        self.PasswordForm.passLines(1)
        confirm = input("Type 'DELETE' to delete your account : ")
        if confirm == "DELETE":
            result = self.db.query("delete from Password where user = ?", (self.User.id,))
            result1 = self.db.query("delete from User where id = ?", (self.User.id,))
            if result['status'] and result1['status']:
                print('account deleted successfully')
                sleep(2)
                return True
            else:
                print(result['message'])
                print(result1['message'])
                sleep(4)
                return False
        else:
            return False
        

    def decryptAll(self, message = "decrypting..."):
        loader = DotLoader(message)
        loader.start()
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
        loader.stop()
        sleep(0.3)

    def home(self, User):
        self.User = User
        available_options = ("insert credential", "view credential", "logout", "Delete Account")
        while True:
            self.PasswordForm.refreshScreen()
            self.PasswordForm.printCenter("> Home <", "=")
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
                elif choice == 3:
                    self.PasswordForm.clearScreen()
                    break
                elif choice ==4:
                    if self.deleteUser():
                        self.PasswordForm.clearScreen()
                        break
                else:
                    continue
            except KeyboardInterrupt:
                self.PasswordForm.clearScreen()
                break
            except ValueError:
                continue