#!/usr/bin/env python3

import socket
from _thread import *
from enum import Enum
from security import *
import rsa

class STATE(Enum):
    START_CLIENT = 1
    WAITING_MESSAGE = 2
    CLOSE_CLIENT = 3

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233
ThreadCount = 0
clients = ()

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..')
ServerSocket.listen(5)

def threaded_client(connection):
    connection.send(str.encode('Welcome to the Server'))
    state = STATE.START_CLIENT
    pubKey = None
    secret_key = generate_secret_key()

    while True:
        try :
            data = connection.recv(1024).decode('utf-8')
            if data == "":
                state = STATE.CLOSE_CLIENT
        except:
            state = STATE.CLOSE_CLIENT

        if state == STATE.START_CLIENT:
            code = data[0:4]
            msg = data[4:]

            if code == "pub:":
                pubKey = rsa.PublicKey.load_pkcs1(bytes(msg, "utf-8"))
                strSecretKey = str(secret_key, "utf-8")
                newMessage = bytes(f"key:{strSecretKey}", "utf-8")
                cipher = rsa.encrypt(newMessage, pubKey)
                connection.sendall(cipher)
                state = STATE.WAITING_MESSAGE

        elif state == STATE.WAITING_MESSAGE:
            data = decrypt_message(str.encode(data), secret_key, str.encode(" "))
            reply = 'Server Says: ' + str(data, "utf-8") + ""
            print(reply)
            reply = encrypt_message(reply, secret_key, " ")
            connection.sendall(reply)
           
        elif state == STATE.CLOSE_CLIENT:
            print(f"Closing socket")
            connection.close()
            break

        
while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
