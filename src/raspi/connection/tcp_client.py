import socket

HOST = "192.168.4.1"
PORT = 23

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print('Connecting to %s port %d' % (HOST, PORT))
    s.connect((HOST, PORT))
    message = input('-> ')
    while message != 'q':
        print('Sending:"%s"' % (message))
        s.send(message.encode('utf-8'))
        data = s.recv(1024)
        print('Recived:"%s"' % (data.decode('utf-8')))
        message = input('-> ')
    print('Closing socket')
    s.close()
