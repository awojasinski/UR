import socket

HOST = '192.168.1.113'
PORT = 10000
MESSAGE = 'Hello world!'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    print('Connecting to %s port %d' %(HOST, PORT))
    s.connect((HOST, PORT))

    try:

        print('Sending:"%s"' %(MESSAGE))
        s.sendall(MESSAGE.encode('utf-8'))

        data = s.recv(1024)
        print('Recived:"%s"' % (data.decode('utf-8')))

    finally:

        print('Closing socket')
        s.close()
