
import base64
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2
import secrets

class Locker:

    BLOCK_SIZE = 16
    salt = "random"

    def pad(self, s):
        return s + (self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE) * chr(self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE)

    def unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]

    def get_private_key(self, password):
        salt = self.salt.encode()
        kdf = PBKDF2(password, salt, 64, 1000)
        key = kdf[:32]
        return key


    def encrypt(self, raw, password):
        private_key = self.get_private_key(password)
        raw = self.pad(raw)
        iv = secrets.token_bytes(AES.block_size)

        cipher = AES.new(private_key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))


    def decrypt(self, enc, password):
        private_key = self.get_private_key(password)
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(private_key, AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(enc[16:])).decode()
