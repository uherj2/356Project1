#!/usr/bin/env python3
# <IP address> <port>
print('client is running')

import socket 
import sys
import time
import threading
data = "Recieved:".encode('utf-8')

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect((sys.argv[1], int(sys.argv[2])))
    #s.connect(('172.18.112.1', 54321))
except TimeoutError:
    print('Timed out connecting to server.')
except Exception as e:
    print(f'Exception while setting up socket and connecting: {e}')
else:
    try:

         while True:

            msg = s.recv(256).decode('utf-8')
            while msg and msg[-1] != '\n':
                msg += s.recv(256).decode('utf-8')

            print(msg)
            if msg.strip()[len(msg.strip())-1] == ':':
                inp1 = input(">> ")
                s.sendall(f'{inp1}\n'.encode('utf-8'))


    except Exception as e:
        print(f'Exception sending: {e}')
finally:
    s.close()
