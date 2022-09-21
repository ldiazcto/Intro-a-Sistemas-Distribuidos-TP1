from socket import *

class Cliente:
    
    

    def __init__(self):
        self.serverName = 'localhost'
        self.serverPort = 12000
        self.clientSocket = socket(AF_INET,SOCK_DGRAM)

    def mandarPaquete(self,paquete):
        self.clientSocket.sendto(paquete.encode(),(self.serverName,self.serverPort))

    def chequearSiLlegoACK():
        paquete = socket.recvfrom(2048)
        return paquete.esACK()

    def cerrarSocket(self):
        self.clientSocket.close()


#forma de pedir por terminal, ej
    #message = input("Input Lower case sentence:")
    
    #mostramos lo reciido por el server
    #print(modifiedMessage.decode())