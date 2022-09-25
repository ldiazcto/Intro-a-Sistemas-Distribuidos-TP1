import threading
from socket import *


class Conexion(threading.Thread):
    def __init__(self,numero_hilo, conexion_cliente):
        threading.Thread.__init__(self)
        self.nombre = numero_hilo
        self.conexion_cliente = conexion_cliente
        self.ip_cliente = conexion_cliente[0]
        self.puerto_cliente = conexion_cliente[1]
        self.skt = socket(AF_INET,SOCK_DGRAM)
        self.queue = []
        self.hay_data = False
        self.conexion_activa = True

    def pasar_data(self, paquete):
        self.queue.append(paquete)
        self.hay_data = True

    def run(self):
        while True:
            if self.conexion_activa == False:
                return
            if self.hay_data: #verifico si me pasaron nueva data
                val = self.queue.pop(0) #obtengo la data
                if len(self.queue) == 0:
                    self.hay_data = False #si la cola queda vacia establezco que no hay mas data, por ahora
                if val is None:   # If you send `None`, the thread will exit.
                    return
                self.imprimir_mensaje(val)
                self.procesar_mensaje(val)
                self.enviar_mensaje()


    def imprimir_mensaje(self, message):
        print ("Numero_hilo:",self.nombre,"conexion:",self.conexion_cliente)
        print ("Mensaje:",message)

    def procesar_mensaje(self,mensaje):
        if mensaje == "FIN":
            print ("CIERRO CONEXION")
            self.conexion_activa = False
    
    def enviar_mensaje(self):
        self.skt.sendto("Respuesta".encode(),(self.ip_cliente,self.puerto_cliente))

    def esta_activa(self):
        return self.conexion_activa