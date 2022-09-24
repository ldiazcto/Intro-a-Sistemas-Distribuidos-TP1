from concurrent.futures import ThreadPoolExecutor
from http import client
from socket import*
import threading
import time 
from queue import Queue
from threading import Thread

""""
def acceptConnection(ServerSocket):
    dictcionario_conexiones{}
    udp_socket.recvv_from(data,direccion)
    if(direccion not in dectionario_conexiones):
        dict[direccion] = new_hilo
        new_hilo.pasar_data(data)
    else:
        dict[direccion].pasar_data(data) 
"""


class mi_hilo():
    def __init__(self,):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.queue = Queue()
    



class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = []
        self.hay_data = False

    def pasar_data(self, paquete):
        self.queue.append(paquete)
        self.hay_data = True

    def run(self):
        while True:
            if self.hay_data:
                val = self.queue.pop(0)
                if len(self.queue) == 0:
                    self.hay_data = False
                if val is None:   # If you send `None`, the thread will exit.
                    return
                self.imprimir_mensaje(val)

    def imprimir_mensaje(self, message):
        print (message)


