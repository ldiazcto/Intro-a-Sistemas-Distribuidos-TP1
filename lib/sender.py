import os
from socket import *
import time
import abc
import select



class Sender(metaclass=abc.ABCMeta):
        #Se establece el handshake y se envía el archivo con el filePath y el fileName pasados durante la creación
        #Se devuelve True si el enviar fue exitoso y False si no
        def enviar_archivo(self,logger):
                filepath= self.filePath + "/" + self.fileName
                file_stats = os.stat(filepath)
                file_size = file_stats.st_size
                handshake_establecido = self.entablarHandshake(self.fileName,file_size)
                if(handshake_establecido):
                        file = open(filepath,'rb')
                        self.enviarPaquetes(file)
                        file.close()
                else:
                        logger.error("Fallo el handshake")


        def crearPaqueteHandshake_upload(self, fileName, fileSize):
                caracterSeparador = self.CARACTER_SEPARADOR
                mensaje = fileName
                mensaje = mensaje + caracterSeparador + str(fileSize)
                return self.gestorPaquetes.crearPaqueteHandshake(self.UPLOAD, mensaje)

 
        def recibirPaquete(self):
                timeout_start = time.time()
                while True:
                        lista_sockets_listos = select.select([self.sender_socekt], [], [], 0)
                        var = time.time()
                        if ((var - timeout_start) >= (self.MAX_WAIT)):
                                return None
                        if not lista_sockets_listos[0]:
                                continue
                        paqueteString, sourceAddress = self.sender_socekt.recvfrom(2048)
                        return self.gestorPaquetes.pasarBytesAPaquete(paqueteString)


        def entablarHandshake(self, fileName, fileSize):
                paquete = self.crearPaqueteHandshake_upload(fileName, fileSize)
                paqueteBytes = self.gestorPaquetes.pasarPaqueteABytes(paquete)
                i = 0
                while i <= self.MAX_TRIES:
                        self.sender_socekt.sendto(paqueteBytes,(self.receiver_ip,self.receiver_port))
                        paqueteRecibido = self.recibirPaquete()                  
                        if (paqueteRecibido == None):
                                i += 1
                                continue
                        esPaqueteOrdenado = self.gestorPaquetes.verificarACK(paqueteRecibido)
                        if (esPaqueteOrdenado) :
                                return True
                        esPaqueteRefused = self.gestorPaquetes.verificarRefused(paqueteRecibido)
                        if (esPaqueteRefused) :
                                return False
                        i +=1

                return False

        @abc.abstractmethod
        def enviarPaquetes(self,file):
                pass


        def enviar_fin(self):
                pck = self.gestorPaquetes.crearPaqueteFin()
                pckBytes = self.gestorPaquetes.pasarPaqueteABytes(pck)
                self.sender_socekt.sendto(pckBytes,(self.receiver_ip,self.receiver_port))
                cantidad_intentos = 1
                paqueteRecibido = self.recibirPaquete()
                while(paqueteRecibido == None and cantidad_intentos <= 3):
                        paqueteRecibido = self.recibirPaquete()
                        cantidad_intentos += 1
                if(cantidad_intentos > 3):
                        return (False,None)
                return (True,paqueteRecibido)