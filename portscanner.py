import threading
from queue import Queue
import time
import socket

# a print_lock is what is used to prevent "double" modification of shared variables.
# this is used so while one thread is using a variable, others cannot access
# it. Once done, the thread releases the print_lock.
# to use it, you want to specify a print_lock per thing you wish to print_lock.
print_lock = threading.Lock()


target = '192.168.0.161'
#ip = socket.gethostbyname(target)


def portscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        con = s.connect((target, port))
        with print_lock:
            print('[OPEN PORTS:]', {port}, '[IP ADDRESS]', {target})
        con.close()
    except:
        pass


# The threader thread pulls an worker from the queue and processes it
def threader():
    while True:
        # gets an worker from the queue
        worker = q.get()
        portscan(worker)
        q.task_done()


# Create the queue and threader
q = Queue()

# how many threads are we going to allow for
for x in range(100):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()


start = time.time()

# 100 jobs assigned.
for worker in range(1, 65536):
    q.put(worker)

# wait until the thread terminates.
q.join()
