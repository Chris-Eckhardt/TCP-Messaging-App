#!/usr/bin/env python3
"""
TCP Client

Name: Chris Eckhardt
ID: 915736372

NOTE: This code only works with python3
"""

# The only socket library allowed for this assignment
import socket
import pickle
import datetime
import sys
import select
import threading

class Client:

    def __init__(self):
        self.HOST = input("Enter the server IP Address: ")
        self.PORT = int(input("Enter the server port: "))
        self.NAME = input("Your id key (i.e. your name): ")
        self.MODE = 0
        self.ID = None
        try:
            self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_sock.connect((self.HOST, self.PORT))
            print("Successfully connected to server with IP: " + self.HOST + " and port: " + str(self.PORT))
        except socket.error as socket_exception:
            print(socket_exception)
            self.client_sock.close()
            exit(1)

        self.send(self.NAME)
        data = self.receive()
        self.ID = data['msg']
        print('id# : ' + str(self.ID))
        #################
        self.run()

    ##############################
    #             RUN            #
    ##############################
    def run(self):
        while True:

            sockets_list = [sys.stdin, self.client_sock]

            read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])
            try:
                for socks in read_sockets:
                    if socks == self.client_sock:
                        data = self.receive()
                        msg = data['msg']
                        if isinstance(msg, list):
                            for s in msg:
                                print(s)
                        else:
                            print(msg)
                    else:
                        message = sys.stdin.readline()
                        self.send(message)
                        sys.stdout.flush()
            except socket.error as socket_exception:
                print(socket_exception)
                break

        print("connection error, closing client...")
        self.client_sock.close()

    ##############################
    #       SEND & RECEIVE       #
    ##############################
    def send(self, msg):
        data = {"from_id": self.ID, "from_name": self.NAME, "msg": msg, "sent_on": datetime.datetime.now()}
        data_serialized = pickle.dumps(data, protocol=2)
        self.client_sock.send(data_serialized)

    def receive(self):
        server_response = self.client_sock.recv(4096)
        if server_response:
            data = pickle.loads(server_response)
            return data
        else:
            print('   !!! CONNECTION TO SERVER WAS LOST !!!  ')
            exit(1)


##################################
#   client process starts here   #
##################################
c = Client()