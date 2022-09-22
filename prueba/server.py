from concurrent.futures import ThreadPoolExecutor
from http import client
from socket import*
import threading
import time 
from queue import Queue
from threading import Thread
import hilo



class server():
    def __init__(self):
        self.conexiones = {}
        serverPort = 12000
        self.serverSocket = socket(AF_INET, SOCK_DGRAM)
        self.serverSocket.bind(('',serverPort))
        self.numero_hilos = 0

    def start(self):
        while True:
            message, clientAdress = self.serverSocket.recvfrom(2048) #tamanio buffer para 1 paquete
            modifiedMessage = message.decode() #decoder paquete
            if(clientAdress not in self.conexiones): #verifico si ya existe la direccion de donde recibi el paquete
                self.conexiones[clientAdress] = hilo.MyThread(self.numero_hilos,clientAdress) #guardo el hilo que se encarga de esa direccion
                self.conexiones[clientAdress].start() #inicio el hilo
                self.numero_hilos += 1
            self.conexiones[clientAdress].pasar_data(modifiedMessage) #le paso la data al hilo
           







