#!/usr/bin/env python3
# <IP address> <port>
print('client is running')

import socket 
import sys
import time

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect((sys.argv[1], int(sys.argv[2])))
except TimeoutError:
    print('Timed out connecting to server.')
except Exception as e:
    print(f'Exception while setting up socket and connecting: {e}')
else:
    try:
         s.sendall(f'Hi this is the client\n'.encode('utf-8'))
    except Exception as e:
        print(f'Exception sending: {e}')
finally:
    s.close()
