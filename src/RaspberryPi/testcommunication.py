import socket
import numpy as np
import struct
import cvis

HOST = '192.168.1.113'
PORT = 10000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(5)

    print('Server |%s|%d|' %(HOST, PORT))

    connection, client_addr = s.accept()

    print('Connection from: ', client_addr)

    pos = np.empty(shape=(0, 2), dtype=np.float32)

    pos[0] = input("Współrzędna X: ")
    pos[1] = input("Współrzędna Y: ")
    data = "(" + str(pos[0]) + "," + str(pos[1]) + ")"

    connection.send(data)

    msg = connection.recv(1024)
    print("Recived: ", msg)

