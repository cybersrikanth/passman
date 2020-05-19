import os
import pickle
import random
import secrets
import getpass
import base64
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2
from hashlib import sha256

BLOCK_SIZE = 16


def pad(s):
    return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)


def unpad(s):
    return s[:-ord(s[len(s) - 1:])]


Login = False
userName = None
PASSWD = None
data = None

capsAlpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
smallAlpha = 'abcdefghijklmnopqrstuvwxyz'
numbers = '0123456789'
specialChar = '!@#()*.<>?/&^%+'

folder = os.environ['HOME'] + '/.passman/'


def retRed(skk):
    return "\033[91m{}\033[00m".format(skk)

# The below code block is under development
# 

class cyberSecret:
    def __init__(self):
        self.rounds = 20
        self.cipher = "csV1"
    def genHash(self, string):
        self.salt = generatePass()
        for i in range(2**self.rounds):
            string = sha256((self.salt + string).encode()).hexdigest()
        string = "${}${}${}${}".format(self.cipher,self.rounds,self.salt,string)
        print(string)
    def compareHash(self,string, hash):
        hash = hash.split("$")
        self.rounds = int(hash[2])
        self.salt = hash[3]
        if hash[1]=="csV1":
            for i in range(2**self.rounds):
                string = sha256((self.salt + string).encode()).hexdigest()
            if string == hash[4]:
                return True
        return False


def changePass():
    test = cyberSecret()
    test.genHash("hello")
    print(test.compareHash("hello","$csV1$20$190#f</1FJ$472dee5a4b4531e66b3272617c6d85dec1e5626ac72e5a997cd841883eb00238"))
    print(test.compareHash("hello","$csV1$20$190#f</1FJ$472dee5a4b4531e66b3272617c6d85dec1e5626ac72e5a997cd841883eb00237"))
    print(test.compareHash("hellO","$csV1$20$190#f</1FJ$472dee5a4b4531e66b3272617c6d85dec1e5626ac72e5a997cd841883eb00237"))
# 
# The above code is under development


def generatePass(length=10):
    mix = (capsAlpha, smallAlpha, numbers, specialChar)
    passwd = [secrets.choice(mix[i]) if i < len(mix) else secrets.choice(mix[random.randint(0, 3)]) for i in
              range(length)]
    random.shuffle(passwd)
    return ''.join(passwd)


def signup(user, passwd):
    if os.path.isfile(folder + user):
        return retRed("user already exist")
    else:
        try:
            with open(folder + user, 'wb') as f:
                pickle.dump([[], sha256((user + passwd).encode()).hexdigest()], f)
            return "Signup Successful"
        except:
            return retRed("Signup failed")


def login(user, passwd):
    global userName, data, Login, PASSWD
    userName = user
    if os.path.isfile(folder + user):
        with open(folder + user, 'rb') as f:
            data = pickle.load(f)
            if data[-1] == sha256((user + passwd).encode()).hexdigest():
                Login = True
                PASSWD = passwd
                return "Login Successful"
            else:
                del data
                return retRed("Password incorrect")
    else:
        return retRed("Invalid User")


def logout():
    global data, Login, userName, PASSWD
    del data, Login, userName, PASSWD
    exit("Logged out Successfully")


class Credentials:

    def __init__(self, website, username, passwd):
        self.website = website
        self.username = username
        self.passwd = passwd

    def fetch(self):
        return {'website': self.website, 'username': self.username, 'passwd': self.passwd}


def savedCredentials():
    global data, PASSWD
    print("\n")
    print("Credentials".center(50, '#'))
    print()
    if len(data[0]) > 0:
        data1 = data[0]
        for index,i in enumerate(data1):
            j = i.fetch()
            print(str(index+1)+") URL =", decrypt(j['website'], PASSWD).decode())
            print("Username =", decrypt(j['username'], PASSWD).decode())
            print("Password =", retRed(decrypt(j['passwd'], PASSWD).decode()))
            print()
        print("#" * 50)
    else:
        print("No saved credentials found")

# def changePass():
#     global data, PASSWD
#     decrypted = []
#     data1 = data[0]
#     for index,datum in enumerate(data1):
#         tmp = {}
#         j = datum.fetch()
#         tmp['website'] = decrypt(j['website'], PASSWD).decode()
#         tmp['username'] = decrypt(j['username'], PASSWD).decode()
#         tmp['passwd'] = decrypt(j['passwd'], PASSWD).decode()
#         decrypted.append(tmp)
#     print(decrypted)


def insertCredential(website, username, update,passwd=''):
    global data, userName, PASSWD
    if len(passwd)==0:
        passwd = generatePass(int(input("Enter length of password to be generated: ")))
    print('your password is:', retRed(passwd))
    i = Credentials(encrypt(website, PASSWD), encrypt(username, PASSWD), encrypt(passwd, PASSWD))
    if not update == None:
        del data[0][update]
    data[0].append(i)
    with open(folder + userName, 'wb') as f:
        pickle.dump(data, f)
    with open(folder + userName, 'rb') as f:
        data = pickle.load(f)
    return True

def deleteCredential():
    index = int(input("Enter index of the credential to be deleted: "))
    global data, userName, PASSWD
    for ind,datum in enumerate(data[0]):
        j = datum.fetch()
        if ind+1 == index:
            print("deleting...",decrypt(j['username'], PASSWD).decode(), retRed("@"), decrypt(j['website'], PASSWD).decode())
            if input("Cannot be undone... type \"yes\" to continue: ") == "yes":
                del data[0][ind]
                with open(folder + userName, 'wb') as f:
                    pickle.dump(data, f)
                with open(folder + userName, 'rb') as f:
                    data = pickle.load(f)
                print("data removed successfully")
                break
            else:
                print("operation cancelled")
                break
    else:
        print("invalid index")


def newCredential():
    global data, PASSWD
    website = input("Enter url/website : ").lower()
    username = input("Enter username : ")
    for x,i in enumerate(data[0]):
        j = i.fetch()
        if website == decrypt(j['website'],PASSWD).decode() and username == decrypt(j['username'],PASSWD).decode():
            print(retRed('Username already exist for this website'))
            print('\t Press',retRed('1'),'to overwrite (This will update password)')
            print('\t Press',retRed('2'),'to cancel')
            try:
                c = int(input("Enter your choice: "))
            except:
                c = 2
                print('Invalid input')
            if c == 1:
                temp = input('Press enter to generate strong password or enter your own password: ')
                if insertCredential(website, username, x, temp):
                    print('\t Password updated successfully')
                else:
                    print(retRed('Error Occured'))
                break
            else:
                print(retRed('operation cancelled'))
                break
    else:
        passwd = input('Press enter to generate strong password or enter your own password: ')
        if insertCredential(website, username, None,passwd):
            print('Data inserted Successfully')
        else:
            print(retRed('Error Occured'))



def get_private_key(password):
    salt = userName.encode()
    kdf = PBKDF2(password, salt, 64, 1000)
    key = kdf[:32]
    return key


def encrypt(raw, password):
    private_key = get_private_key(password)
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))


def decrypt(enc, password):
    private_key = get_private_key(password)
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))


options = {
    1: savedCredentials,
    2: newCredential,
    3: deleteCredential,
    4: logout,
    5: changePass
}

while not Login:
    if not os.path.isdir(folder):
        os.mkdir(folder)
    print(retRed('-') * 50)
    print("Welcome to password manager \n\tEnter your credentials to login \n\t\tleave blank user name to signup\n")
    print(retRed('-') * 50)
    print("Login".center(50, '#'))
    uName = input("Enter username: ")
    if not uName == '':
        mPass = getpass.getpass(prompt='Master Password: ', stream=None)
        print(login(uName, mPass))
    else:
        print()
        print("Signup".center(50, '#'))
        uName = input("Enter your username: ")
        mPass1 = getpass.getpass(prompt='Enter new Master Password: ', stream=None)
        mPass2 = getpass.getpass(prompt='Confirm Master Password: ', stream=None)
        if uName != '' and mPass1 == mPass2 and len(mPass1) > 7:
            print(signup(uName, mPass1))
        else:
            print(retRed("Password doesnt match or too short or Username is null"))
            print(retRed("Try again......"))
while Login:
    print("\nWelcome", userName)
    print("\nChoose your option...")
    print("1 --- View all saved credentials")
    print("2 --- Create or update credential")
    print("3 --- delete credential")
    print("4 --- Logout and Exit")
    print("5 --- change password")
    try:
        choice = int(input("Enter your choice: "))
        options[choice]()
    except (KeyError, ValueError):
        print(retRed("Invaid option.... Please try again"))
        continue
