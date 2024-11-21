#!/usr/bin/env python3

print('file is executing')

import sys
import socket
import threading
import time

id = set([])

def add_connection_id(connectionid):
    id.add(connectionid)
    print(f'id added {id}')
    time.sleep(60)
    id.remove(connectionid)
    print(f'id removed {id}')


def handle_connection(cs, addr):
    try: 
        print(f'cs: {cs}')
        print(f'addr: {addr}')
        msg = cs.recv(256).decode('utf-8')
        while msg and msg[-1] != '\n':
            msg += cs.recv(256).decode('utf-8')
        print(msg)

        if msg[0].isdigit():
            connectionid = int(msg[0])
            if connectionid in id:
                cs.send(f'connection id already in use\n'.encode(utf-8))
                print(f'connection id already in use')
            else:
                idthread = threading.Thread(target=add_connection_id, args=[connectionid])
                idthread.daemon = True
                idthread.start()
                cs.send(f'your connection id is: {connectionid}'.encode('utf-8'))
    except Exception as e:
        print(f'Exception while receiving or sending: {e}')
    finally:
        print("connection close happened")
        cs.close()


try:    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # This says hey you can reuse the socket after the program is done
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.settimeout(90)
    s.bind(('', int(sys.argv[1])))
    print(f'listening on port {int(sys.argv[1])}')
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
