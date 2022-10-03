import os
from pickle import FALSE
import threading
import time
import gestorPaquetes
import receiver
from socket import *
import paquete
import stopAndWait
import goBackN
from pathlib import Path
import sender_stop_wait_server
import sender_gobackn_server



DATA = 0 #a veces llamado NOT_ACK
ACK = 1
UPLOAD = 2
DOWNLOAD = 3
REFUSED = 4
FIN = 5
ACK_CORRECT = 1
ACK_INCORRECT = 0

MAX_WAIT_HANDSHAKE = 30
MAX_TAMANIO_PERMITIDO = 5000000 #en bytes
MAX_WAIT_SERVIDOR = 50 #PELIGRO! TIMEOUT DEL SERVER!!


class Receiver(threading.Thread):
    def __init__(self, ip_cliente,port_cliente,filePath,filename):
        threading.Thread.__init__(self)
        self.ip_cliente = ip_cliente
        self.puerto_cliente = port_cliente #por ac'a escribe o escucha el cliente? --> ambos 
        self.skt = socket(AF_INET,SOCK_DGRAM)
        self.queue = []
        self.hay_data = False
        self.conexion_activa = True
        self.gestor_paquete = gestorPaquetes.Gestor_Paquete()
        self.filePath = filePath
        self.Termino = False

    def pasar_data(self, paquete= b""):
        self.queue.append(paquete)
        self.hay_data = True

    def run(self):
        print("Path de archivos",self.filePath)
        print("Largo del path es:",len(self.filePath))
        #file_stats = os.stat(self.filePath)
        #file_size = file_stats.st_size
        file = open(self.filePath,'wb')
        self.recibir_archivo(file)
        self.Termino = True
        file.close()
        



    def imprimir_mensaje(self, paqueteBytes):
        #print ("Numero_hilo: ",self.nombre,"conexion:",self.conexion_cliente)
        print ("paqueteBytes: ",paqueteBytes)
        print("\n")

    def procesar_mensaje(self,paqueteBytes,file):
        paquete = self.gestor_paquete.pasarBytesAPaquete(paqueteBytes)

        print("El paqueteBytes recibido en procesar_mensaje es = ", paqueteBytes)
        print("El mensaje es recibido en procesar_mensaje es = ", paquete.obtenerMensaje())

        if (self.gestor_paquete.verificarPaqueteOrdenado(paquete) == True):
            if(paquete.esFin()):
                
                print("ES PAQUETE FIN: ")
                paquete_ack = self.gestor_paquete.crearPaqueteACK(ACK_CORRECT)
                print("El paquete ACK que voy a mandar por haber entrado a True es: ", self.gestor_paquete.pasarPaqueteABytes(paquete_ack))
                #time.sleep(10)
                self.skt.sendto(self.gestor_paquete.pasarPaqueteABytes(paquete_ack),(self.ip_cliente,self.puerto_cliente))
                print("Envié el paquete ACK positivo a esta ip y puerto ", (self.ip_cliente,self.puerto_cliente))
                self.Termino = True
                self.conexion_activa = False
                return

            print("Al verificar el paquete, resulta que es True")
            paquete_ack = self.gestor_paquete.crearPaqueteACK(ACK_CORRECT)
            file.write(paquete.obtenerMensaje())
            print("El paquete ACK que voy a mandar por haber entrado a True es: ", self.gestor_paquete.pasarPaqueteABytes(paquete_ack))
            #time.sleep(10)
            self.skt.sendto(self.gestor_paquete.pasarPaqueteABytes(paquete_ack),(self.ip_cliente,self.puerto_cliente))
            print("Envié el paquete ACK positivo a esta ip y puerto ", (self.ip_cliente,self.puerto_cliente))
        else:
            print("Al verificar el paquete, resulta que es False")
            paquete_ack = self.gestor_paquete.crearPaqueteACK(ACK_INCORRECT)
            print(self.gestor_paquete.pasarPaqueteABytes(paquete_ack))
            #time.sleep(2)
            self.skt.sendto(self.gestor_paquete.pasarPaqueteABytes(paquete_ack),(self.ip_cliente,self.puerto_cliente))
        
    def esta_activa(self):
        return self.conexion_activa


    def recibir_archivo(self,file):
        time_start = time.time()
        while time.time() - time_start <=   MAX_WAIT_SERVIDOR:
            #print(time.time() - time_start)
            if self.conexion_activa == False:
                return
            if self.hay_data: #verifico si me pasaron nueva data
                time_start = time.time()
                paqueteBytes = self.queue.pop(0) #obtengo la data
                #print("\n\n-- En recibi_archivo, el paqueteBytes recien recibido es: ", paqueteBytes)
                if len(self.queue) == 0:
                    self.hay_data = False #si la cola queda vacia establezco que no hay mas data, por ahora
                if paqueteBytes is None:   # If you send `None`, the thread will exit.
                    return
                self.imprimir_mensaje(paqueteBytes)
                self.procesar_mensaje(paqueteBytes,file)
                #print("Volvi de procesar_mensaje, el paqueteBytes era: ", paqueteBytes)
                #print("\n\n")
        print("ESPERE SUFICIENTE NO ME MANDASTE NADA")
        self.conexion_activa = False
        self.Termino = True
        return
    
   