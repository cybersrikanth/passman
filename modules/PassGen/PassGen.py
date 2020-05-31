import random

class PassGen:
    password = []
    charset = {
        "lower":"abcdefghijklmnopqrstuvwxyz",
        "upper":"ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "number":"0123456789",
        "special":"!@#$%^&*()-_+=<>,./?[{]}|:;"
    }

    def __init__(self):
        self.length = 10
        self.allow = ("lower", "upper", "number", "special")
        self.shuffle = True

    def generate(self):
        allowLength = len(self.allow)
        for i in range(int(self.length)):
            if i< allowLength:
                chars = self.charset[self.allow[i]]
            else:
                chars = self.charset[self.allow[random.randrange(0,allowLength)]]
            self.password.append(chars[random.randrange(0,len(chars))])
        if(self.shuffle):
            random.shuffle(self.password)
        return "".join(self.password)

