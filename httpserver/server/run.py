# -*- coding: utf-8 -*-
import socket
import http_generator
import http_form


def get_response(request):
    response = http_generator.generate_http_response(request)
    return bytes(str(response), encoding='utf-8')


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 8000))  # make our server to listen to localhost on port 8000
server_socket.listen(3)  # set max queue length for the socket

print('Started')

while 1:
    try:
        (client_socket, address) = server_socket.accept()
        print('Got new client', client_socket.getsockname())  # print client name
        request_string = client_socket.recv(2048)  # read 2048 bytes from client socket
        print(request_string)
        client_socket.send(get_response(request_string))  # create response to the request and send it back to a client
        client_socket.close()
    except KeyboardInterrupt:  # if program is interrupted by a keyboard the following block will be executed.
        print('Stopped')
        server_socket.close()  # stop listen to localhost:8000 and terminate the server
        exit()
