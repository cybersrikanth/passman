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
        for i in data1:
            j = i.fetch()
            print("Website or URL =", decrypt(j['website'], PASSWD).decode())
            print("Username =", decrypt(j['username'], PASSWD).decode())
            print("Password =", retRed(decrypt(j['passwd'], PASSWD).decode()))
            print()
        print("#" * 50)
    else:
        print("No saved credentials found")


def newCredential():
    global data, Login, userName, PASSWD
    website = input("Enter url/website : ").lower()
    username = input("Enter username : ")
    passwd = generatePass(int(input("Enter length of password to be generated: ")))
    print('generated password is:', retRed(passwd))
    i = Credentials(encrypt(website, PASSWD), encrypt(username, PASSWD), encrypt(passwd, PASSWD))
    data[0].append(i)
    with open(folder + userName, 'wb') as f:
        pickle.dump(data, f)
    with open(folder + userName, 'rb') as f:
        data = pickle.load(f)


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
    3: logout
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
    print("2 --- Create new credential")
    print("3 --- Logout and Exit")
    try:
        choice = int(input("Enter your choice: "))
        options[choice]()
    except (KeyError, ValueError):
        print(retRed("Invaid option.... Please try again"))
        continue
