# NAME: 
    CHRIS ECKHARDT
# ID: 
    915736372

# Project name: 
    TCP Message App
    
# Grade 

100/100. Plus 1% of extracredit for implementing threading in the new channel option. Extracredit will be added at the end of the semester to your final grade 

Comments: 

• Really good program. Perfectly implemented. Your code looks good too. 

• Chris, first of all, congratulations for the good program your submitted. Secondly, I have read your insights about the challenges of the projects, and I am glad you found the sockets assignment easy. However, you need to understand that this is not a OOD class. This is an upper division class, and students are expected to know already how to structure their programs once they are given the program guidelines. My job is not teaching students how class interfaces work together. However, I did that in class. Maybe, you missed that class. In addition, you had nine pages of documentation with clear guidelines about how to do that.
   
# Project description: 
    This project is TCP messaging applicaiton. One instance of the 
    Server will run on a machine connected to a network. At least one 
    client instance will run on another machine also in that network.
    Once the client connects to the server a client handler thread will
    be spawned by the server. This handler will respond to all clinet requests.
    The main thread will continue listening for additional client connections.

# Project purpose:
    The purpose of this assignment is to learn how sockets are 
    used by processes to send data back and forth over a network.
    By creating a multithreaded server-client applicaiton, we can 
    demonstrate how multiple end points can communicate.

# How to clone and run program:
    Open a linux terminal and navigate to the directory you would like to have the
    project folder in. Once there, type ...
    'git clone https://github.com/sfsu-joseo/csc645-01-fall2019-projects-Chris-Eckhardt.git'
    Next navigate to '/applicaitons/tcp-message-app' within the project directory.
    Now in this termial, enter the command 'python3 server.py' and the server will run.
    Next open another terminal window and navigate to the same folder. Now type the
    command 'python3 client.py'

# Compatibility issues: 
    You must use python3 when running this applicaiton. The code used 
    is only compatable with version 3 and newer.

# Summary
    In this project I found that the threading and working with sockets was the easy part.
    The difficulty came when implimenting the structure of the Handler and how it connects.
    I spent the past two weeks writing the handler class and then erasing it once I realised 
    it wouldnt work. Then redoing and redoing it. I wish the instructions had a clearer sense 
    of how the class instances were supposed to work together since the point of the assignment
    was to work with sockets. I actually spent very little time working with the actual sockets 
    because they always seemed to work and caused very little issues. 
    In conclusion, this assingment was a good warm-up for the future assingments of this class.
    I wish I had approached the archetecture differently and planned it out before trying to 
    impliment it. This was a good learning experience for the multitude of reasons previously listed.
