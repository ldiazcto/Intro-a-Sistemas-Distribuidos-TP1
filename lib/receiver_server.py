from asyncio import SendfileNotAvailableError
import os
from pickle import FALSE
import threading
import time
import gestorPaquetes
import receiver
from socket import *
import paquete
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

    def __init__(self, ip_cliente,port_cliente,filePath,filename,logger):
        threading.Thread.__init__(self)
        self.ip_cliente = ip_cliente
        self.puerto_cliente = port_cliente 
        self.skt = socket(AF_INET,SOCK_DGRAM)
        self.queue = []
        self.hay_data = False
        self.conexion_activa = True
        self.gestor_paquete = gestorPaquetes.Gestor_Paquete()
        self.filePath = filePath
        self.Termino = False
        self.fileName = filename
        self.logger = logger

    def pasar_data(self, paquete= b""):
        self.queue.append(paquete)
        self.hay_data = True

    def run(self):
        fileCompleto = self.filePath + "/" + self.fileName
        file = open(fileCompleto,'wb')
        self.recibir_archivo(file)
        self.Termino = True
        file.close()
        
    def procesar_mensaje(self,paqueteBytes,file):
        paquete = self.gestor_paquete.pasarBytesAPaquete(paqueteBytes)
        if (self.gestor_paquete.verificarPaqueteOrdenado(paquete) == True):
            if(paquete.esFin()):         
                paquete_ack = self.gestor_paquete.crearPaqueteACK(ACK_CORRECT)
                try:
                    self.skt.sendto(self.gestor_paquete.pasarPaqueteABytes(paquete_ack),(self.ip_cliente,self.puerto_cliente))
                except SendfileNotAvailableError:
                    self.logger.error("-- El archivo no esta disponible --")
                self.logger.info(f"Envié el paquete ACK positivo a esta ip y puerto:{self.ip_cliente} {self.puerto_cliente}")
                self.Termino = True
                self.conexion_activa = False
                return
            paquete_ack = self.gestor_paquete.crearPaqueteACK(ACK_CORRECT)
            file.write(paquete.obtenerMensaje())
            try:
                self.skt.sendto(self.gestor_paquete.pasarPaqueteABytes(paquete_ack),(self.ip_cliente,self.puerto_cliente))
            except SendfileNotAvailableError:
                self.logger.error("-- El archivo no esta disponible --")
            self.logger.info(f"Envié el paquete ACK positivo a esta ip {self.ip_cliente} y puerto: {self.puerto_cliente}")
        else:
            self.looger.debug(":( El paquete ACK a enviar es negativo")
            paquete_ack = self.gestor_paquete.crearPaqueteACK(ACK_INCORRECT)
            try:
                self.skt.sendto(self.gestor_paquete.pasarPaqueteABytes(paquete_ack),(self.ip_cliente,self.puerto_cliente))
            except SendfileNotAvailableError:
                self.logger.error("-- El archivo no esta disponible --")
                
    def esta_activa(self):
        return self.conexion_activa


    def recibir_archivo(self,file):
        time_start = time.time()
        while time.time() - time_start <=  MAX_WAIT_SERVIDOR:
            if self.conexion_activa == False:
                return
            if self.hay_data:
                time_start = time.time()
                paqueteBytes = self.queue.pop(0) 
                if len(self.queue) == 0:
                    self.hay_data = False 
                if paqueteBytes is None:   
                    return
                self.procesar_mensaje(paqueteBytes,file)
        self.logger.error("✗ Timeout al recibir el archivo...")
        self.conexion_activa = False
        self.Termino = True
        return
    
   