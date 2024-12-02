#!/usr/bin/env python3
# <IP address> <port>
print('client is running')

import socket 
import sys
import time
import threading
import json

data = "Recieved:".encode('utf-8')

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
                loggedIn = True
            elif msg.strip()[len(msg.strip())-1] == ':':
                inp1 = input(">> ")
                s.send(f'{inp1}\n'.encode('utf-8'))


         running = True
         while running == True:
            #read last message
            time.sleep(1)
            msg = s.recv(256).decode('utf-8')
            print(msg)

            rec = input("Enter recipient or type 'STOP':\n")
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
