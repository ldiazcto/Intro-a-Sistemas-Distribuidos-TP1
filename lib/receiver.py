import time
from socket import *
import gestorPaquetes
import os
import select


ACK = 1
DOWNLOAD = 3
REFUSED = 4
FIN = 5
ACK_CORRECT = 1
ACK_INCORRECT = 0

MAX_TRIES = 3
MAX_WAIT = 10

MAX_WAIT_SERVIDOR = 50 #PELIGRO! TIMEOUT DEL SERVER!!

class Receiver():  
    
    def __init__(self, sender_ip, sender_port, file_path, file_name, logger ):
        self.receiver_socekt = socket(AF_INET,SOCK_DGRAM)
        self.receiver_socekt.setblocking(False)
        self.sender_ip = sender_ip
        self.sender_port = sender_port
        self.gestor_paquete = gestorPaquetes.Gestor_Paquete()
        self.Termino = False
        self.file_path = file_path
        self.file_name = file_name
        self.logger = logger


    # Dados el path y el file name enviados al constructor, se entabla el handshake y se recibe el archivo
    # Se devuelve True en caso de éxito y False en caso de error
    def recibir_archivo(self):
        new_path = self.file_path + "/" + self.file_name
        filepath= new_path
        handshake_establecido = self.entablarHandshake(self.file_name)
        if(handshake_establecido):
            file = open(filepath,'wb')
            self.recibir_Paquetes(file)
            file.close()
            return True
        else:
            self.logger.error("El handshake ha fallado...")
            return False


    def recibir_Paquetes(self,file):
        time_start = time.time()
        while time.time() - time_start <=   MAX_WAIT_SERVIDOR:
            lista_sockets_listos = select.select([self.receiver_socekt], [], [], 0)
            if(self.Termino == True):
                return
            if not lista_sockets_listos[0]:
                continue
            paqueteBytes, sourceAddress = self.receiver_socekt.recvfrom(2048)
            time_start = time.time()
            self.procesar_mensaje(paqueteBytes,file)
        self.logger.error("Timeout...")

    def procesar_mensaje(self,paqueteBytes,file):
        paquete = self.gestor_paquete.pasarBytesAPaquete(paqueteBytes)

        if (self.gestor_paquete.verificarPaqueteOrdenado(paquete) == True):
            if(paquete.esFin()):
                self.Termino = True
                paquete_ack = self.gestor_paquete.crearPaqueteACK(ACK_CORRECT)
                self.receiver_socekt.sendto(self.gestor_paquete.pasarPaqueteABytes(paquete_ack),(self.sender_ip,self.sender_port))
                self.logger.info(f"Se envio el paquete ACK positivo a este ip y puerto{self.sender_ip} {self.sender_port}")
                file.close()
                self.conexion_activa = False
                return

            paquete_ack = self.gestor_paquete.crearPaqueteACK(ACK_CORRECT)
            file.write(paquete.obtenerMensaje())
            self.receiver_socekt.sendto(self.gestor_paquete.pasarPaqueteABytes(paquete_ack),(self.sender_ip,self.sender_port))
        else:
            paquete_ack = self.gestor_paquete.crearPaqueteACK(ACK_INCORRECT)
            self.receiver_socekt.sendto(self.gestor_paquete.pasarPaqueteABytes(paquete_ack),(self.sender_ip,self.sender_port))

    def crearPaqueteHandshake_download(self, fileName):
        return self.gestor_paquete.crearPaqueteHandshake(DOWNLOAD, fileName)


    def entablarHandshake(self, fileName):
        paquete = self.crearPaqueteHandshake_download(fileName)
        paqueteBytes = self.gestor_paquete.pasarPaqueteABytes(paquete)
        i = 0
        while i <= MAX_TRIES:
                self.receiver_socekt.sendto(paqueteBytes,(self.sender_ip,self.sender_port))
                paqueteRecibido = self.recibirAckHandshake()
                if (paqueteRecibido == None):
                        i += 1
                        continue
                esPaqueteOrdenado = self.gestor_paquete.verificarACK(paqueteRecibido)
                if (esPaqueteOrdenado) :
                        return True
                esPaqueteRefused = self.gestor_paquete.verificarRefused(paqueteRecibido)
                if (esPaqueteRefused) :
                        return False
                i +=1

        return False

    
    def recibirAckHandshake(self):
        timeout_start = time.time()
        while True:
                lista_sockets_listos = select.select([self.receiver_socekt], [], [], 0)
                var = time.time()
                if ((var - timeout_start) >= (MAX_WAIT)):
                        return None
                if (self.Termino == True):
                    return
                if not lista_sockets_listos[0]:
                        continue
                paqueteString, sourceAddress = self.receiver_socekt.recvfrom(2048)
                return self.gestor_paquete.pasarBytesAPaquete(paqueteString)