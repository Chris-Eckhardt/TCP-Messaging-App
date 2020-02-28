#!/usr/bin/env python3
"""
TCP Client Handler

Name: Chris Eckhardt
ID: 915736372

NOTE: This code only works with python3
"""

import socket
import pickle
import datetime
import time


class TCPClientHandler:

    mode = 0
    MENU = '****** TCP CHAT ******\n-----------------------\nOptions Available:\n1. Get user list\n2. Send a ' \
           'message\n3. Get my messages\n4. Create a new channel\n5. Chat in a channel with your friends\n6. ' \
           'Disconnect from server\n\nYour option <enter a number>: '

    def __init__(self, client, client_id, server):
        self.client = client 
        self.client_id = client_id
        self.server = server
        self.chat_name = None
        self.mode = 0
        # receive client username
        data = self.receive()
        self.username = data['msg']
        # send client their id
        self.send(self.client_id[1], 0)
        self.server.log('Client ' + self.username + ' with clientid: ' + str(client_id[1]) + ' has connected to this server')
        

    
    ##############################
    #            RUN             #
    ##############################
    def run(self):

        ####################################
        #             main loop            #
        ####################################
        while True:

            ####################################
            #             Menu Mode            #
            ####################################
            if self.mode == 0:

                # send menu
                self.send(self.MENU, 0)

                flag = False
                while not flag:

                    data = self.receive()
                    choice = data['msg']
                    try:
                        choice = int(choice)
                        flag = True
                    except ValueError:
                        self.send('*** invalid input ***', -1)

                if 0 < choice < 7:

                    if choice == 1:  # send user list
                        self.send(self.server.get_user_list(self.client_id), 0)
                        time.sleep(0.2)
                        self.send('\npress ENTER to continue...', 0)
                        enter = None
                        while not enter:
                            enter = self.receive()

                    elif choice == 2:  # send a message
                        self.send('What is the id# of the person you would like to send a message to? ', self.mode)
                        target = msg = None
                        while not target:
                            target = self.receive()
                        self.send('What would you like to say to user ' + target['msg'].rstrip('\n') + '? ', self.mode)
                        while not msg:
                            msg = self.receive()
                        self.server.send_a_message(self.username, self.client_id[1], target['msg'].rstrip('\n'), msg['msg'].rstrip('\n'), self.mode)

                    elif choice == 3:  # get waiting messages
                        self.server.get_messages(self.client_id, self.mode)
                        time.sleep(0.2)
                        self.send('\npress ENTER to continue...', self.mode)
                        enter = None
                        while not enter:
                            enter = self.receive()

                    elif choice == 4: # make a new channel
                        self.send('What would you like to name this channel', self.mode)
                        data = None
                        while not data:
                            data = self.receive()
                        self.chat_name = data['msg']
                        self.server.create_new_chat(self.chat_name, self.client_id)
                        self.server.log('client ' + str(self.client_id[1]) + ' created a new channel called ' + self.chat_name)
                        self.mode = 1
                        time.sleep(0.5)
                        self.send('-------------- CHANNEL --------------\n type "exit()" to leave the chat', self.mode)
                        
                    elif choice == 5: # join the chat
                        self.send('What channel would you like to join?', self.mode)
                        data = None
                        while not data:
                            data = self.receive()
                        self.chat_name = data['msg'] 
                        if not (self.server.join_chat(self.chat_name, self.client_id)):
                            time.sleep(0.5)
                            self.send("No channel exists..", self.mode)
                            continue
                        else:
                            time.sleep(0.5)
                            self.mode = 1
                            self.send('-------------- CHANNEL --------------\n type "exit()" to leave the chat', self.mode)
                        

                    elif choice == 6: # diconnect from server
                        self.client.close()
                        self.server.remove_client(self.client_id)
                        exit(0)

                else:
                    # the input is not valid
                    self.send('*** invalid input ***', -1)
            
            ####################################
            #             Chat Mode            #
            ####################################
            if self.mode == 1:
                data = self.receive()
                if data:
                    chat_post = data['msg']
                    name = data['from_name']
                    if chat_post == 'exit()\n':
                        self.mode = 0
                        self.server.leave_chat(self.chat_name, self.client_id)
                        self.chat_name = None
                        time.sleep(0.5)
                        continue
                    msg = '<' + name + '>: ' + chat_post
                    self.server.post_to_chat(self.chat_name, msg)
            
            time.sleep(0.5)
    
    ##############################
    #       SEND & RECEIVE       #
    ##############################
    def send(self, msg, mode):
        data = {'from_id': self.client_id, 'from_name': self.username, 'msg': msg, 'mode': mode}
        data_serialized = pickle.dumps(data, protocol=2)
        self.client.send(data_serialized)

    def receive(self):
        request_from_client = self.client.recv(4096)
        if request_from_client:
            data = pickle.loads(request_from_client)
            return data
        else:
            self.server.log(str(self.client_id[1]) + ' has disconnected from the server...')
            # delete client here!!!
            self.server.remove_client(self.client_id)
            exit(1)