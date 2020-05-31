from . import Form
from modules.PassGen import PassGen

class PasswordForm(Form):
    def __init__(self):
        pass

    def newCredential(self, credential):
        pending = True
        credential.website = input("Website : ")
        credential.username = input("username : ")
        while pending:
            password = input("press enter to generate password or enter your password : ")
            if(len(password)):
                credential.password = password
                pending = False
            else:
                self.clearLines(2)
                try:
                    length = int(input("Enter length of password : "))
                    passgen = PassGen()
                    passgen.length = length
                    credential.password = passgen.generate()
                    pending = False
                except:
                    pending = True
                    self.clearLines(2)


