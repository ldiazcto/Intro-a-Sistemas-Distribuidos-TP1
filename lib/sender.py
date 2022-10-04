import os
from socket import *
import time
import abc
import select

MAX_TRIES = 3


class Sender(metaclass=abc.ABCMeta):
        def enviar_archivo(self,logger):
                filepath= self.filePath + "/" + self.fileName
                file_stats = os.stat(filepath)
                file_size = file_stats.st_size
                logger.debug("Se está por entablar el handshake...")
                handshake_establecido = self.entablarHandshake(self.fileName,file_size)
                if(handshake_establecido):
                        logger.info("✓ Se estableció el hanshake con éxito")
                        file = open(filepath,'rb')
                        self.enviarPaquetes(file)
                        file.close()
                else:
                        logger.error("✗ Fallo el handshake")


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
                                self.logger.debug(f"✗ Vez {i} de máxima {MAX_TRIES} en que no se recibió el handshake")
                                i += 1
                                continue
                        esPaqueteOrdenado = self.gestorPaquetes.verificarACK(paqueteRecibido)
                        if (esPaqueteOrdenado) :
                                self.logger.debug("✓ Se recibió el ACK esperado")
                                return True
                        esPaqueteRefused = self.gestorPaquetes.verificarRefused(paqueteRecibido)
                        if (esPaqueteRefused) :
                                self.logger.debug("✗ No se recibió el ACK esperado")
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
                while(paqueteRecibido == None and cantidad_intentos <= MAX_TRIES):
                        paqueteRecibido = self.recibirPaquete()
                        cantidad_intentos += 1
                if(cantidad_intentos > MAX_TRIES):
                        self.logger.error(f"Se intentó enviar el mismo paquete más de {MAX_TRIES} veces")
                        return (False,None)
                return (True,paqueteRecibido)