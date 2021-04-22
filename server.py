#!/usr/bin/env python3
import socket
from _thread import *
from enum import Enum
from security import *

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
    connection.send(str.encode('Welcome to the Servern'))
    state = STATE.WAITING_MESSAGE
    pubKey = None
    secret_key = gen_sym_key()

    while True:
        try :
            data = connection.recv(2048).decode('utf-8')
        except:
            state = STATE.CLOSE_CLIENT

        if state == STATE.START_CLIENT:
            code = data[0:4]
            msg = data[4:]

            if code == "pub":
                pubKey = msg
                connection.sendall(str.encode(encrypt_with_symkey(secret_key, f"sym:{secret_key}")))
                state = STATE.WAITING_MESSAGE

        elif state == STATE.WAITING_MESSAGE:
            data = decrypt_with_symkey(secret_key, data)
            reply = 'Server Says: ' + data + ""
           
            connection.sendall(str.encode(encrypt_with_symkey(secret_key, reply)))
        elif state == STATE.CLOSE_CLIENT:
            connection.close()
            break

        
while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))

ServerSocket.close()
