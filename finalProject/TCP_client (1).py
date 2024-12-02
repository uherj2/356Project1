#!/usr/bin/env python3
# <IP address> <port>
print('client is running')

import socket 
import sys
import time
import threading
import json
import random

data = "Recieved:".encode('utf-8')

def memory_Allocation(s):
    for i in range(1,10):
        time.sleep(4)
        if i%2==1:
            data = {"action": "allocate", "size":random.randint(128,2048)}
            print(f"Request: {data}")
        else:
            data = {"action": "deallocate","address":random.randint(0,100)}
            print(f"Request: {data}")
        json_packet = json.dumps(data)
        s.send(f'{json_packet}\n'.encode('utf-8'))
        time.sleep(3)
        msg = s.recv(256).decode('utf-8')
        print(msg)


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    #s.connect((sys.argv[1], int(sys.argv[2])))
    s.connect(('172.18.112.1', 54321))
except TimeoutError:
    print('Timed out connecting to server.')
except Exception as e:
    print(f'Exception while setting up socket and connecting: {e}')
else:
    try:
         loggedIn = False
         while loggedIn == False:

            msg = s.recv(256).decode('utf-8')

            print(msg)
            if msg.strip() == "Successfully signed into server":
                print("Signing in!")
                loggedIn = True
            elif msg.strip()[len(msg.strip())-1] == ':':
                inp1 = input(">> ")
                s.send(f'{inp1}\n'.encode('utf-8'))

         print("Starting Memory Allocation")
         memThread = threading.Thread(target=memory_Allocation, args=[s])
         memThread.daemon = True
         memThread.start()
         running = True
         while running == True:
            #read last message
            time.sleep(1)
            print('.')
            msg = s.recv(256).decode('utf-8')
            print(msg)

            rec = input("Enter recipient or type 'STOP' or type 'READ':\n")
            if rec == "STOP":
                data = {"action": "stop"}
                json_packet = json.dumps(data)
                s.send(f'{json_packet}\n'.encode('utf-8'))
                running == False
                print("All Done!")
                break
            else:
                msg = input("Enter Message:\n")
                data = {"action":"message","recipient":rec,"message":msg}
                json_packet = json.dumps(data)
                s.send(f'{json_packet}\n'.encode('utf-8'))
                #checks for message

    except Exception as e:
        print(f'Exception sending: {e}')
finally:
    s.close()
