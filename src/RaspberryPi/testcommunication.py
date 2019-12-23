import socket
import numpy as np
import struct


HOST = '192.168.0.110'
PORT = 10000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(5)

    print('Server |%s|%d|' %(HOST, PORT))

    connection, client_addr = s.accept()

    print('Connection from: ', client_addr)
    msg = connection.recv(1024)
    print("Recived: ", msg)
    connection.send('(-0.437, -0.545, 0.537, 0, 3.14, 0)'.encode('ascii'))

