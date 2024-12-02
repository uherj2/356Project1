#!/usr/bin/env python3

print('file is executing')

import sys
import socket
import threading
import time
import hashlib
import json

#database
user_db = {}  # username: hashed_password

with open('user_db.json', 'w') as file:
    json.dump(user_db, file, indent=4)

active_users = {}  # username: connection_id

active_connections = {} # username : cs

# lock for thread-safety
db_lock = threading.Lock()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# store new user in db with hashed password
def store_user(username: str, password: str):
    with db_lock:
        #loads user_db from file
        with open('user_db.json', 'r') as file:
            user_db = json.load(file)
        if username in user_db:
            return "Username already exists"
        # hash and store password
        user_db[username] = hash_password(password)
        #writes new user_db into file
        with open('user_db.json', 'w') as file:
            json.dump(user_db, file, indent=4)
        return f"User {username} added successfully"

def verify_user(username: str, password: str) -> bool:
    with db_lock:
        # loads user_db from file
        with open('user_db.json', 'r') as file:
            user_db = json.load(file)
        if username not in user_db:
            print("failed username check")
            return False
        # compare hashed password
        return user_db[username] == hash_password(password)

# add to active users with connection id
def add_active_user(username: str, connection_id: int, cs):
    with db_lock:

        if username in active_users:
            return f"User {username} is already active"
        active_users[username] = connection_id
        active_connections[username] = cs
        return f"User {username} is now active with connection id {connection_id}"

def del_active_user(username: str):
    with db_lock:
        # loads user_db from file
        with open('user_db.json', 'r') as file:
            user_db = json.load(file)
        if username in active_users:
            del active_users[username]
            # writes new user_db into file
            with open('user_db.json', 'w') as file:
                json.dump(user_db, file, indent=4)
            return f"User {username} removed from active users"
        else:
            return f"User {username} not found in active users"

# get connection id of active user
def get_cID(username: str):
    with db_lock:
        return active_users.get(username, None)

# lists users if needed
def list_active_users():
    with db_lock:
        return active_users

# simulate segmentation/paging
def mem_allocation(username: str, block_size: int = 256):
    # loads user_db from file
    with open('user_db.json', 'r') as file:
        user_db = json.load(file)
    # simulate segmentation by allocating blocks
    mem_block = {
        "username": username,
        "block_size": block_size,
        "allocated_data": user_db.get(username, None)
    }
    return mem_block

# simulate retrieving user memory block
def get_user_mem_block(username: str):
    # loads user_db from file
    with open('user_db.json', 'r') as file:
        user_db = json.load(file)
    # return user data from 'db'
    if username in user_db:
        return mem_allocation(username)
    else:
        return None
#end database

store_user("Username","Password")
id = set()

def send_all(message):
    for connectionid in id:
        cs = connectionid[1]
        print(f'cs: {cs}')
        cs.send(f'{message}:\n'.encode('utf-8'))

def send_user(message, recipient):
    cs = active_connections[recipient]
    print(f'cs: {cs}')
    cs.send(f'{message}:\n'.encode('utf-8'))

def add_connection_id(connectionid):
    id.add(connectionid)
    print(f'id added {id}')
    time.sleep(60)
    id.remove(connectionid)
    print(f'id removed {id}')

def handle_connection(cs, addr):
    try:
        cs.send("Enter Connection ID:\n".encode('utf-8'))
        print(f'cs: {cs}')
        print(f'addr: {addr}')
        msg = cs.recv(256).decode('utf-8')
        while msg and msg[-1] != '\n':
            msg += cs.recv(256).decode('utf-8')
        print(msg)

        if msg[0].isdigit():
            connectionid = (int(msg[0]), cs)
            if connectionid[0] in (item[0] for item in id):
                cs.send(f'connection id already in use\n'.encode('utf-8'))
                print(f'connection id already in use')
            else:
                idthread = threading.Thread(target=add_connection_id, args=[connectionid])
                idthread.daemon = True
                idthread.start()
                cs.send(f'your connection id is: {connectionid[0]}\n'.encode('utf-8'))
                #send_all(connectionid[0])
                time.sleep(1)
        #sign in or sign up
        prompt = True
        while prompt == True:
            cs.send("Type 'Sign in' or 'Sign up':\n".encode('utf-8'))
            ans = cs.recv(256).decode('utf-8')
            if ans.strip() == "Sign up":
                cs.send("Enter New Username:\n".encode('utf-8'))
                usr = cs.recv(256).decode('utf-8')
                usr = usr.strip()
                print(usr)

                if usr in user_db:
                    cs.send("Error: username already exists\n".encode('utf-8'))
                # handling Password
                else:
                    cs.send("Enter New Password:\n".encode('utf-8'))
                    psw = cs.recv(256).decode('utf-8')
                    psw = psw.strip()
                    print(psw)
                    print("User added")
                    #adding new user into the system
                    store_user(usr, psw)
                    add_active_user(usr, connectionid[0], connectionid[1])
                    cs.send("Successfully signed into server\n".encode('utf-8'))
                    # exit loop
                    prompt = False
            elif ans.strip() == "Sign in":
                # handling Username
                cs.send("Enter Username:\n".encode('utf-8'))
                usr = cs.recv(256).decode('utf-8')
                usr = usr.strip()
                print(usr)
                # handling Password
                cs.send("Enter Password:\n".encode('utf-8'))
                psw = cs.recv(256).decode('utf-8')
                psw = psw.strip()
                print(psw)
                if verify_user(usr, psw):
                    print("User verified")
                    add_active_user(usr, connectionid[0], connectionid[1])
                    cs.send("Successfully signed into server\n".encode('utf-8'))
                    # exit loop
                    prompt = False
                else:
                    cs.send("Wrong Password or Username! Try again!\n".encode('utf-8'))
                    print("closed connection")
                    cs.close()
            else:
                cs.send("Error: neither option selected correctly.\n".encode('utf-8'))
        #sending messages
        running = True
        while running == True:
            cs.send(f"Active Users: {list_active_users()}\n".encode('utf-8'))
            print(".")
            #cs.send("Enter recipient or type 'STOP':\n".encode('utf-8'))
            json_packet = cs.recv(256).decode('utf-8')
            print(".")
            data = json.loads(json_packet)
            print(data)
            if data['action']=="message":
                rec = data['recipient']
                rec = rec.strip()
                if rec in active_users:
                    msg  = data['message']
                    msg = msg.strip()
                    print(rec,msg)
                    send_user(msg,rec)
                else:
                    cs.send(f"User {rec} is not active:\n".encode('utf-8'))
            elif data['action']=="stop":
                print("User stopped")
                running = False
            else:
                print("JSON Packet ERROR")
                cs.send("JSON Packet ERROR!:\n".encode('utf-8'))



    except Exception as e:
        print(f'Exception while receiving or sending: {e}')
    finally:
        print("connection close happened")
        #return
        cs.close()


try:    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # This says hey you can reuse the socket after the program is done
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.settimeout(90)
    #s.bind(('', int(sys.argv[1])))
    s.bind(('172.18.112.1',54321))
    #print(f'listening on port {int(sys.argv[1])}')
    print(f'listening on port {65432}')
    s.listen(5)  # 5 is the number of connections to keep in a queue
except Exception as e:
    print(f'Exception while setting up socket: {e}')
else:
    try:
        while True:
            cs, addr = s.accept()
            try:
                t = threading.Thread(target=handle_connection, args=[cs, addr])
                t.daemon = True
                t.start()
            except Exception as e:
                print(f'Exception occurred accepting or creating a thread to handle connection: {e}')
    except TimeoutError:
        print('Timed out waiting for connections')
    except Exception as e:
        print(f'An exception occurred: {e}')
finally:
    s.close()

