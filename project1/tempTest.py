from asyncio import Semaphore
import time
from datetime import datetime
from _356Project1 import Car
import random
import threading

start_time = time.time()


global rows, cols
rows, cols = (2, 10)
arr = [[0 for i in range(cols)] for j in range(rows)]

arr[0][0] = 1
arr[1][0] = 2

car_1 = Car(0, 1, arr)
car_2 = Car(1, 2, arr)

t1 = threading.Thread(target=car_1.start)
t2 = threading.Thread(target=car_2.start)

t1.start()
t2.start()
