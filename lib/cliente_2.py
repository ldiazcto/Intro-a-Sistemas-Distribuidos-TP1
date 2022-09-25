from socket import *

class Cliente:
    
    

    def __init__(self):
        self.serverName = 'localhost'
        self.serverPort = 12000
        self.clientSocket = socket(AF_INET,SOCK_DGRAM)

    def mandarPaquete(self,paquete=b""):
        print ("mandar_paquete",paquete)
        self.clientSocket.sendto(paquete,(self.serverName,self.serverPort))

    def chequearSiLlegoACK(self):
        paquete,addres = self.clientSocket.recvfrom(2048)
        print( paquete )
       

    def cerrarSocket(self):
        self.clientSocket.close()


#forma de pedir por terminal, ej
    #message = input("Input Lower case sentence:")
    
    #mostramos lo reciido por el server
    #print(modifiedMessage.decode())

