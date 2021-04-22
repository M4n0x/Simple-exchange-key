import os

AES_KEY_LENGTH = 16

def gen_sym_key():
    return os.urandom(AES_KEY_LENGTH) # TEMPORARY

def encrypt_with_symkey(symkey, msg):
    return "encrypt symkey not implemented yet"

def decrypt_with_symkey(symkey, msg):
    return "decrypt with symkey not implemented yet"