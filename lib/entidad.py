from abc import ABC, abstractclassmethod, abstractmethod
from socket import *
import time
import stopAndWait
import select

UPLOAD = 2
MAX_TRIES = 2
MAX_WAIT = 10
NOT_BLOCKING= 0 
BLOCKING = 1
MAX_WAIT_RESPONSE = 10

class Entidad(ABC):

        def __init__(self,name, miPuerto, puertoEntradaContrario):
                self.name = name #el nombre de a quien le envía esta entidad
                self.puertoEntradaContrario = puertoEntradaContrario #el port de entrada del contrario (si por ejemplo est'as instanciando un cliente, este es el puerto por donde escucha el servidor)
                self.entidadSocket = socket(AF_INET,SOCK_DGRAM)
                self.entidadSocket.bind(('',miPuerto))



#para la subida


        def crearPaqueteHandshake(self, fileName, fileSize, operador):
                caracterSeparador = "-"
                mensaje = fileName
                if (operador == UPLOAD) :
                        mensaje = mensaje + caracterSeparador + str(fileSize)
                else:
                        x=1
                        #falta la lógica donde se agrega lo necesario para el download
                return self.gestorPaquetes.crearPaqueteHandshake(operador, mensaje)


        def entablarHandshake(self, fileName, fileSize, operador):
                paquete = self.crearPaqueteHandshake(fileName, fileSize, operador)
                paqueteBytes = self.gestorPaquetes.pasarPaqueteABytes(paquete)
                i = 0
                env = stopAndWait.StopAndWait()
                while i <= MAX_TRIES:
                        self.enviarPaquete(paqueteBytes)
                        paqueteRecibido = self.recibirPaquete()
                        #TIMEOUTEA VUELVO A ENVIAR EL HANDSHAKE
                        if (paqueteRecibido == None):
                                print(i)
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


        def enviarPaquete(self,pckBytes):
                self.entidadSocket.sendto(pckBytes ,(self.name,self.puertoEntradaContrario))
        
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
                        print("recibirPaquete: el string del paquete es: ", paqueteString)
                        return self.gestorPaquetes.pasarBytesAPaquete(paqueteString)

        def recibirPaqueteBackN(self):
                self.entidadSocket.setblocking(False)
                lista_sockets_listos = select.select([self.entidadSocket], [], [], 0)
                if not lista_sockets_listos[0]:
                        return None
                paqueteString, sourceAddress = self.entidadSocket.recvfrom(2048)
                print("recibirPaquete: el string del paquete es: ", paqueteString)
                return self.gestorPaquetes.pasarBytesAPaquete(paqueteString)
                """
                try :
                        paqueteString, sourceAddress = self.entidadSocket.recvfrom(2048)
                        self.entidadSocket.setblocking(BLOCKING)
                        return self.gestorPaquetes.pasarBytesAPaquete(paqueteString)
                except BlockingIOError:
                        return None
                """

        def recibirArchivo(self, ruta):
            #pensarla, tal vez puede ser genérica
                x = 1

        def cerrarSocket(self):
                self.entidadSocket.close()
        