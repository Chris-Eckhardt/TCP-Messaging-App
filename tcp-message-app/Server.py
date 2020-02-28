#!/usr/bin/env python3
"""
TCP Server

Name: Chris Eckhardt
ID: 915736372

NOTE: This code only works with python3
"""

import socket
import pickle
import datetime
import threading

import TCPClientHandler


####################################
#           Server Class           #
####################################
class Server:
    HOST = '127.0.0.1'       # this is just to run on local host
    PORT = 12000             # this can be anything >10000
    ADDR = (HOST, PORT)
    MAX_CLIENTS = 10
    LOCK = threading.Lock()
    client_list = []         # holds client handlers, messages, and other info
    thread_list = []         # this hold all thread, makes for easy joining, however the program will probably never reach that point
    chat_list = []           # 

    ####################################
    #            Server init           #
    ####################################
    def __init__(self):
        # open socket and listen
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind(self.ADDR)
            # listen for new connections
            self.sock.listen(self.MAX_CLIENTS)
            print('Server Info')
            print('IP address : ' + self.HOST)
            print('Port listening : ' + str(self.PORT))
            print("Waiting for connections... ")
        except socket.error as socket_exception:
            print(socket_exception)
            self.sock.close()

        # wait for clients
        while True:
            client, client_id = self.sock.accept()
            handler = TCPClientHandler.TCPClientHandler(client, client_id, self)
            client_thread = threading.Thread(target=handler.run)
            client_thread.start()
            self.thread_list.append(client_thread)
            self.client_list.append(ClientStruct(client, client_id, handler))

        # join threads
        for thread in self.thread_list:
            thread.join()

        # close server socket
        self.sock.close()
    # end __init__()


    ####################################
    #     server helper methods        #
    ####################################    
    def log(self, entry):
        self.LOCK.acquire()
        print(entry)
        self.LOCK.release()

    def get_user_list(self, client_id):
        temp = []
        for profile in self.client_list:
            temp.append(str(profile.client_id[1]) + '      <' + profile.handler.username + '>')
        self.log('List of users sent to client: ' + str(client_id[1]))
        return temp

    def send_a_message(self, sender_name, sender_id, target, msg, mode):
        # look up target from client list
        for profile in self.client_list:
            if int(target) == profile.client_id[1]:
                self.LOCK.acquire()
                profile.messages.append(str(datetime.datetime.now()) + ' : <' + sender_name + '> ' + msg)
                self.LOCK.release()
                break
            else:
                continue
        # send the clients handler instructions
        self.log('message to:   ' + str(target) + ' : from : ' + str(sender_id))

    def get_messages(self, client_id, mode):
        for profile in self.client_list:
            if client_id[1] == profile.client_id[1]:
                if len(profile.messages) > 0:
                    profile.handler.send(profile.messages, 2)
                    self.log('List of messages sent to user ' + str(client_id[1]))
                    break
                else:
                    profile.handler.send('You have no new messages.', 3)
                    break

    def get_client_profile(self, client_id):
        for profile in self.client_list:
            if client_id[1] == profile.client_id[1]:
                return profile

    def remove_client(self, id):
        # in case the client_thread is holding the LOCK
        self.LOCK.acquire(False)
        self.LOCK.release()
        for profile in self.client_list:
            if id[1] == profile.client_id[1]:
                self.LOCK.acquire()
                self.client_list.remove(profile)
                self.LOCK.release()
                self.log('Client ' + str(id[1]) + ' disconnected from server')
    

    ################################### 
    #       Chat helper methods       #
    ###################################    
    def create_new_chat(self, chat_name , client_id):
        self.LOCK.acquire()
        new_chat = Chat(self, chat_name, client_id)
        self.chat_list.append(new_chat)
        self.LOCK.release()
        self.log(str(client_id[1]) + ' has joined the chat : ' + chat_name)

    def join_chat(self, chat_name, client_id):
        if self.find_chat(chat_name):
            self.find_chat(chat_name).add_member(client_id)
            self.log(str(client_id[1]) + ' has joined the chat : ' + chat_name)
            return True
        else:
            return False

    def leave_chat(self, chat_name, client_id):
        self.LOCK.acquire()
        self.find_chat(chat_name).remove_member(client_id)
        self.LOCK.release()
        self.log(str(client_id[1]) + ' has left the chat : ' + chat_name)


    def find_chat(self, chat_name):
        for chat in self.chat_list:
            if chat.chat_name == chat_name:
                return chat

    def post_to_chat(self, chat_name, msg):
        self.find_chat(chat_name).chat_post(msg)


####################################
#           Chat struct            #
####################################
class Chat:

    LOCK = threading.Lock()
    members = []

    def __init__(self, server, chat_name, client_id):
        self.server = server
        self.chat_name = chat_name
        self.add_member(client_id)

    def chat_post(self, msg):
        for m in self.members:
            profile = self.server.get_client_profile(m)
            profile.handler.send(msg, 5)

    def add_member(self, client_id):
        self.members.append(client_id)
        self.chat_post(str(client_id[1]) + ' joined the chat.')

    def remove_member(self, client_id):
        for m in self.members:
            if client_id[1] == m[1]:
                client_name = self.server.get_client_profile(client_id).handler.username
                self.chat_post(client_name + ' has left the chat ' + self.chat_name)
                self.members.remove(m)

    
####################################
#          Client struct           #
####################################
class ClientStruct:

    def __init__(self, client, client_id, handler):
        self.messages = []
        self.client = client
        self.client_id = client_id
        self.handler = handler


####################################
#          Main Function           #
####################################
def main():
    Server()
    exit(0)


if __name__ == '__main__':
    main()