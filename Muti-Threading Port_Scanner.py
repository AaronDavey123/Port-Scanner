import socket
import threading
import queue

ip = '10.8.2.198'
q = queue.Queue()

#Storing port numbers in our queue
for i in range(1, 1001):
    q.put(i)

def scan():
    while not q.empty():
        port = q.get()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((ip, port))
                print(f'port {port} is open!')
            except:
                pass
            q.task_done()


# Create number of threads we want to use
for i in range(500):
    t = threading.Thread(target=scan, daemon=True)
    t.start()

q.join()
print("Finished")