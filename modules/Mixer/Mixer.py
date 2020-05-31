from hashlib import sha256
from modules.PassGen import PassGen

class Mixer:
    def __init__(self):
        self.rounds = 20
        self.cipher = "mix1"

    def mix(self, string):
        passGen = PassGen()
        passGen.allow = ("lower", "upper", "number")
        self.salt = passGen.generate()
        for i in range(2**self.rounds):
            string = sha256((self.salt + string).encode()).hexdigest()
        string = "${}${}${}${}".format(self.cipher,self.rounds,self.salt,string)
        return string

    def verify(self,string, hash):
        hash = hash.split("$")
        self.rounds = int(hash[2])
        self.salt = hash[3]
        if hash[1]=="mix1":
            for i in range(2**self.rounds):
                string = sha256((self.salt + string).encode()).hexdigest()
            if string == hash[4]:
                return True
        return False