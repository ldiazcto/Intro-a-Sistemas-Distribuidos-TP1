from abc import ABC, abstractclassmethod, abstractmethod
from socket import *
import time
import stopAndWait
import select

UPLOAD = 2
MAX_TRIES = 2
MAX_WAIT = 1
NOT_BLOCKING= 0 
BLOCKING = 1
MAX_WAIT_RESPONSE = 10

class Entidad(ABC):

        def __init__(self,name,port):
                self.name = name #el nombre de a quien le envía esta entidad
                self.port = port #el port de a quién le envía esta entidad
                self.entidadSocket = socket(AF_INET,SOCK_DGRAM)



#para la subida


        def crearPaqueteHandshake(self, fileName, fileSize, operador):
                caracterSeparador = "-"
                mensaje = fileName
                if (operador == UPLOAD) :
                        mensaje = mensaje + caracterSeparador + str(fileSize)
                return self.gestorPaquetes.crearPaqueteHandshake(operador, mensaje)


        def entablarHandshake(self, fileName, fileSize, operador):
                paquete = self.crearPaqueteHandshake(fileName, fileSize, operador)
                paqueteBytes = self.gestorPaquetes.pasarPaqueteABytes(paquete)
                i = 0
                env = stopAndWait.StopAndWait()
                while i <= MAX_TRIES:
                        #VER COMO RESOLVER PORQUE EL HANDSHAKE NO SE MANDA EN STOP AND WAIT
                        #LINEA DE ABAJO ES UN BUUUGGGG !!!!!
                        #env.enviarPaqueteHandshake(self, paqueteBytes)
                        self.enviarPaquete(paqueteBytes) #MANDO HANDSHAKE DE FORMA COMUN 
                        paqueteRecibido = self.recibirPaquete()
                        esPaqueteOrdenado = self.gestorPaquetes.verificarACK(paqueteRecibido)
                        if (esPaqueteOrdenado) :
                                return True
                        esPaqueteRefused = self.gestorPaquetes.verificarRefused(paqueteRecibido)
                        if (esPaqueteRefused) :
                                return False
                        i +=1

                return False


        def enviarPaquete(self,pckBytes):
                self.entidadSocket.sendto(pckBytes ,(self.name,self.port))
        
        def enviarArchivo(self, file, enviador):
            enviador.enviarPaquete(file, self)

        
        def recibirPaquete(self):
                timeout_start = time.time()
                self.entidadSocket.setblocking(False)
                while True:
                        lista_sockets_listos = select.select([self.entidadSocket], [], [], 0)
                        var = time.time()
                        if ((var - timeout_start) >= (MAX_WAIT)):
                                return None
                        if not lista_sockets_listos[0]:
                                continue
                        paqueteString, sourceAddress = self.entidadSocket.recvfrom(2048)
                        return self.gestorPaquetes.pasarBytesAPaquete(paqueteString)

        def recibirPaqueteBackN(self,timeout):
                timeActual = time.time()
                self.entidadSocket.setblocking(NOT_BLOCKING)
                try :
                        paqueteString, sourceAddress = self.entidadSocket.recvfrom(2048)
                        self.entidadSocket.setblocking(BLOCKING)
                        return self.gestorPaquetes.pasarBytesAPaquete(paqueteString)
                except BlockingIOError:
                        if(timeout > timeActual + MAX_WAIT_RESPONSE):
                                return None
                
      

        def recibirArchivo(self, ruta):
            #pensarla, tal vez puede ser genérica
                x = 1

        def cerrarSocket(self):
                self.entidadSocket.close()
        