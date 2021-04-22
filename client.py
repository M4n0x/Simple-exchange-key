#!/usr/bin/env python3

import socket
import enum
import time
import rsa

pub, priv = rsa.newkeys(1024)

class ConnectionState(enum.Enum):
    CONNECTING = 0
    STARTED = 1
    WAITING_KEY = 2
    NORM = 3
    ENDED = 4

state = ConnectionState.CONNECTING

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233

cryptKey = ""

while True:
    # Connection
    if state == ConnectionState.CONNECTING:
        try:
            print(f"Connecting to {host}:{port}")
            ClientSocket.connect((host, port))
            print(ClientSocket.recv(1024))
            print("Connected")
            state = ConnectionState.STARTED
        except socket.error as e:
            time.sleep(1)
            pass

    # Send public key
    elif state == ConnectionState.STARTED:
        print("Sending pub key")
        pubStr = str(pub.save_pkcs1(), "utf-8")
        ClientSocket.send(str.encode(f"pub:{pubStr}"))
        state = ConnectionState.WAITING_KEY

    # Receive symetric key
    elif state == ConnectionState.WAITING_KEY:
        message = str(ClientSocket.recv(1024), "utf-8").split(":")
        print(message)
        if not message[0] == "key":
            state = ConnectionState.ENDED
        else:
            cryptKey = message[1]
            state = ConnectionState.NORM

    elif state == ConnectionState.ENDED:
        ClientSocket.close()
        break

