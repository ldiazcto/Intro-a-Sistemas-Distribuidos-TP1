from abc import ABC, abstractclassmethod, abstractmethod
from socket import *

class Entidad(ABC):

        def __init__(self,name,port):
                self.name = name
                self.port = port
                self.entidadSocket = socket(AF_INET,SOCK_DGRAM)


#para la subida

        @abstractmethod
        def enviarPaquete(self, mensaje):
                pass

        def enviarArchivo(self, ruta, enviador):
            file = enviador.abrirArchivo(ruta)
            enviador.enviarPaquete(file, self)

        
        @abstractmethod
        def recibirPaquete(self):
                #pensarla, para descargar paquetes
                return

        def recibirArchivo(self, ruta):
            #pensarla, tal vez puede ser genérica
                x = 1

        #lo necesitamos pero todavía no está implementado
        #def chequearSiLlegoACK(): #cambiar nombre de funcion
        #    paquete_string = socket.recvfrom(2048)
        #    return paquete.esACK(), paquete.obtenerACK()


        def cerrarSocket(self):
                self.clientSocket.close()
        