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
                                print("Cliente: Recibí un ack ordenado!")
                                return True
                        esPaqueteRefused = self.gestorPaquetes.verificarRefused(paqueteRecibido)
                        print ("PAaquete Refuse es:",esPaqueteRefused)
                        if (esPaqueteRefused) :
                                print("Cliente: el server rechazó la conexión :_(")
                                return False
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
                self.entidadSocket.setblocking(False)
                while True:
                        lista_sockets_listos = select.select([self.entidadSocket], [], [], 0)
                        var = time.time()
                        if ((var - timeout_start) >= (MAX_WAIT)):
                                print ("var es", var)
                                print ("timeout_start es", timeout_start)
                                print ("timeout_start + MAX_WAIT es:", timeout_start + MAX_WAIT)
                                print ("var - timeout_start es: ", var - timeout_start)
                                return None
                                #volver a mandar_mensaje
                        if not lista_sockets_listos[0]:
                                #print ("ENTRON ACA NUNCA LEO")
                                continue
                        paqueteString, sourceAddress = self.entidadSocket.recvfrom(2048)
                        return self.gestorPaquetes.pasarBytesAPaquete(paqueteString)

        def recibirPaqueteBackN(self):
                self.entidadSocket.setblocking(NOT_BLOCKING)
                try :
                        paqueteString, sourceAddress = self.entidadSocket.recvfrom(2048)
                        #self.entidadSocket.setblocking(BLOCKING)
                        return self.gestorPaquetes.pasarBytesAPaquete(paqueteString)
                except BlockingIOError:
                        self.entidadSocket.setblocking(BLOCKING)
                        return None
                
      

        def recibirArchivo(self, ruta):
            #pensarla, tal vez puede ser genérica
                x = 1

        def cerrarSocket(self):
                self.clientSocket.close()
        