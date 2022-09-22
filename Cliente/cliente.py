from socket import *
from Enviador.stopAndWait import StopAndWait
from Paquetes import *
from Enviador import *

NOT_ACK = -1

class Cliente:
    
    def __init__(self):
        self.serverName = 'localhost'
        self.serverPort = 12000
        self.clientSocket = socket(AF_INET,SOCK_DGRAM)
        self.sequenceNumberActual = 0
 
    def mandarPaquete(self,mensaje):
        paquete = paquete(sequenceNumberActual, NOT_ACK, mensaje)
        sequenceNumberActual += 1
        self.clientSocket.sendto(paquete.encode(),(self.serverName,self.serverPort))

    def subirArchivo(self,ruta):
        enviador = StopAndWait(self)
        file = enviador.leerArchivo(ruta)
        enviador.enviarPaquete(enviador, file)
       
    def chequearSiLlegoACK(): #cambiar nombre de funcion
        paquete = socket.recvfrom(2048)
        return paquete.esACK(), paquete.obtenerACK()

    def cerrarSocket(self):
        self.clientSocket.close()


#forma de pedir por terminal, ej
    #message = input("Input Lower case sentence:")
    
    #mostramos lo reciido por el server
    #print(modifiedMessage.decode())

