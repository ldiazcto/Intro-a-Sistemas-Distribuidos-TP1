from abc import ABC, abstractclassmethod, abstractmethod
from socket import *
import time
import stopAndWait
import select

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
                env = stopAndWait.StopAndWait()
                while i <= MAX_TRIES:
                        env.enviarPaqueteHandshake(self, paqueteBytes)
                        paqueteRecibido = self.recibirPaquete()
                        esPaqueteOrdenado = self.gestorPaquetes.verificarACK(paqueteRecibido)
                        if (esPaqueteOrdenado) :
                                print("Cliente: Recibí un ack ordenado!")
                                return True
                        print("Cliente: No recibí un ack o no fue ordenado, intento ", i)
                        i +=1

                print("Cliente: sali del while en el intento ", i)
                return False


        def enviarPaquete(self,pckBytes):
                self.entidadSocket.sendto(pckBytes ,(self.name,self.port))
        
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
        