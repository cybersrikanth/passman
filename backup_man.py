from Crypto import Random
from Crypto.Cipher import AES
from hashlib import md5
import sys
from passman_gdrive_client import main

def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

def encrypt(message, key, key_size=256):
    message = pad(message)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(message)

def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b"\0")

def encrypt_file(file_name, key):
    with open(file_name, 'rb') as fo:
        plaintext = fo.read()
    enc = encrypt(plaintext, key)
    with open(file_name + ".enc", 'wb') as fo:
        fo.write(enc)

def decrypt_file(file_name, key):
    with open(file_name, 'rb') as fo:
        ciphertext = fo.read()
    dec = decrypt(ciphertext, key)
    with open(file_name[:-4], 'wb') as fo:
        fo.write(dec)

if not len(sys.argv) == 2:
    print("required exactly one argument push/pull")
    exit()

arg = sys.argv[1]

key = md5(input("Enter password, You can leave blank : ").encode()).digest()

if arg == "push":
    encrypt_file('passman.db', key)
    main("push")
elif arg == "pull":
    main("pull")
    decrypt_file('passman.db.enc', key)
else:
    print("invalid arg passed")