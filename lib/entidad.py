from abc import ABC, abstractclassmethod, abstractmethod
from socket import *
import time
import enviador

UPLOAD = 2
MAX_TRIES = 2
MAX_WAIT = 0.5

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
                while i <= MAX_TRIES:
                        self.enviador.enviarPaqueteHandshake(self, paqueteBytes)
                        paqueteRecibido = self.recibirPaquete()
                        if paqueteRecibido == None:
                                print("Debería entrar acá, intento ", i)
                                return False 
                        
                        esPaqueteOrdenado = self.gestorPaquetes.verificar_mensaje_recibido(paqueteRecibido)
                        if (esPaqueteOrdenado) :
                                return True
                        i +=1

                print("Sali del while, debería estar acá, i vale ", i)
                return False

        @abstractmethod
        def enviarPaquete(self, mensaje):
                pass

        def enviarArchivo(self, file, enviador):
            enviador.enviarPaquete(file, self)

        
        def recibirPaquete(self):
                timeout_start = time.time()
                while True:
                        lista_sockets_listos = select.select([self.entidadSocket], [], [], 1)
                        var = time.time()
                        if (var >= (timeout_start + MAX_WAIT)):   
                                return None
                                #volver a mandar_mensaje
                        if not lista_sockets_listos[0]:
                                continue
                        paqueteString, sourceAddress = self.entidadSocket.recvfrom(2048)
                        return self.gestorPaquetes.pasarBytesAPaquete(paqueteString)

        def recibirArchivo(self, ruta):
            #pensarla, tal vez puede ser genérica
                x = 1

        def cerrarSocket(self):
                self.clientSocket.close()
        