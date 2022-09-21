from concurrent.futures import ThreadPoolExecutor
from http import client
from socket import*
import threading
import time 
from queue import Queue
from threading import Thread

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('',serverPort))

#Tratamos al servidor 

#while True:
#    message, clientAdress = serverSocket.recvfrom(2048)
#    modifiedMessage = message.decode().upper()
#    serverSocket.sendto(modifiedMessage.encode(),clientAdress)


#def connectDistribute():
#La idea atras de este es ser la primer conexion que distribuya los primeros paquetes a los otros puertos



#def recieve():
#La idea atras de esta es ser la que hace la conexion al puerto disponible y asi establecer la conexion y comunicacion
#Osea esta es la funcion que le paso al thread dentro del threadpool para que establezca conexion y se quede en el while recibiendo

#def send():
#La idea atras de esta es ser la que hace la conexion al puerto disponible y asi establecer la conexion y comunicacion
#Osea esta es la funcion que le paso al thread dentro del threadpool para que establezca conexion y se quede en algun loop mandando 
#hasta terminarse el archivo, deberia ser muy parecida a la que usa el cliente PERO es importante que el servidor cambie de puerto


#executor = ThreadPoolExecutor(max_workers= 6)

def clientHandler(port, host): #No se bien si aca invocamos la funcion o se la damos por parametro para recibir/guardar o para mandar/sacar
    try:
        serverSocket.bind((host,port))
    except socket.error as e:
        print("error culero")

    while True:
        #if caso de fin cerrar conexion
        serverSocket.close()
            #Mandar mensaje o de alguna forma sacar direccion del diccionario
        
        #if caso primera conexion devuelvo ack confirmando

        #if caso queres descargar

        #if caso de queres subir algo

def startServer(host,port):
    #lista de puertos disponibles y el diccionario que tenga el cliente, el thread y el puerto asociado
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    diccionarioConexiones = {}
    
    try:
        serverSocket.bind((host,port))
    except socket.error as e:
        print("error culero")

    while True:
        message, clientAdress = serverSocket.recvfrom(2048) #tamanio buffer para 1 paquete
        modifiedMessage = message.decode() #decoder paquete
        if(direccion not in dectionarioConexiones):
            dectionarioConexiones[direccion] = clientAdress
            serverSocket.sendto(paquete) #paquete siendo el ack con el nuevo puerto
            #stop and wait solo para el ack de este paquete asi me confirma que recibio a donde conectarse confirmo que me llega
            newThread = Thread(clientHandler,port,host) #siendo el host el mismo y el puerto uno de los disponibles

        #Si la direccion esta caso error

#--------------------------------------------------------------------------------------------------------------------------------------------


def acceptConnection(ServerSocket):
    dictcionario_conexiones{}
    udp_socket.recvv_from(data,direccion)
    if(direccion not in dectionario_conexiones):
        dict[direccion] = new_hilo
        new_hilo.pasar_data(data)
    else:
        dict[direccion].pasar_data(data) 



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


