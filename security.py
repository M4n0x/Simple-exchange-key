import os, base64
import rsa
from Crypto.Cipher import AES

# https://gist.github.com/syedrakib
def generate_secret_key():
	AES_key_length = 16 # use larger value in production
	secret_key = os.urandom(AES_key_length)
	encoded_secret_key = base64.b64encode(secret_key)
	return encoded_secret_key

def encrypt_message(private_msg, encoded_secret_key, padding_character):
	secret_key = base64.b64decode(encoded_secret_key)
	cipher = AES.new(secret_key)
	padded_private_msg = private_msg + (padding_character * ((16-len(private_msg)) % 16))
	encrypted_msg = cipher.encrypt(padded_private_msg)
	encoded_encrypted_msg = base64.b64encode(encrypted_msg)
	return encoded_encrypted_msg

def decrypt_message(encoded_encrypted_msg, encoded_secret_key, padding_character):
	secret_key = base64.b64decode(encoded_secret_key)
	encrypted_msg = base64.b64decode(encoded_encrypted_msg)
	cipher = AES.new(secret_key)
	decrypted_msg = cipher.decrypt(encrypted_msg)
	unpadded_private_msg = decrypted_msg.rstrip(padding_character)
	return unpadded_private_msg

def gen_rsa():
	return rsa.newkeys(1024)

def decrypt_rsa(msg, priv):
	return rsa.decrypt(msg, priv)

def encrypt_rsa(msg, pub):
	return rsa.encrypt(msg, pub)
