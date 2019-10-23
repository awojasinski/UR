import socket

HOST = '192.168.1.113'
PORT = 10000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))

    print('Server | host %s | port %d |' % (HOST, PORT))
    s.listen(1)
    s.settimeout(5)

    while True:
        print("Waiting for connection")
        try:
            connection, client_addr = s.accept()
            print("Connection from", client_addr)
            while True:
                data = connection.recv(1024)
                if not data:
                    print("No more data from: ", client_addr)
                    print('Closing connection')
                    connection.close()
                    break
                print('Received:"%s"' %(data))
                print('Sending data back')
                connection.sendall(data)
        except socket.timeout as e:
            print(e, ': no connection for 5 seconds...')
            print("Closing server")
            s.close()
            break
