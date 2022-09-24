from sender.stopAndWait import StopAndWait
from socket import *
#from Pck.paquete import *


NOT_ACK = -1

class Cliente:
    

    def __init__(self, serverName, serverPort):
        self.serverName = serverName
        self.serverPort = serverPort
        self.clientSocket = socket(AF_INET,SOCK_DGRAM)
        self.sequenceNumberActual = 0
        print("Llegue a crear el cliente")
 
    def mandarPaquete(self,mensaje):
        #modificamos para probar el server, pero se deberia mandar paquete
        #paquete = paquete(sequenceNumberActual, NOT_ACK, mensaje)
        #sequenceNumberActual += 1
        #self.clientSocket.sendto(paquete.encode(),(self.serverName,self.serverPort))
        self.clientSocket.sendto(mensaje,(self.serverName,self.serverPort))


    def subirArchivo(self,ruta):
        stopWait = StopAndWait(self)
        file = stopWait.abrirArchivo(ruta)
        stopWait.enviarPaquete(stopWait, file)

    def descargarArchivo(self,ruta):
        #pensarla
        x = 1
    
    #lo necesitamos pero todavía no está implementado
    #def chequearSiLlegoACK(): #cambiar nombre de funcion
    #    paquete_string = socket.recvfrom(2048)
    #    paquete = pickle.algo(paquete_string)
    #    return paquete.esACK(), paquete.obtenerACK()

    def cerrarSocket(self):
        self.clientSocket.close()


#forma de pedir por terminal, ej
    #message = input("Input Lower case sentence:")
    
    #mostramos lo reciido por el server
    #print(modifiedMessage.decode())

