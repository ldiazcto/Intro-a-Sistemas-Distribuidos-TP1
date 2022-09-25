from socket import *
import entidad

NOT_ACK = -1

class Cliente(entidad.Entidad):
    
    def __init__(self, name, port):
        super(entidad.Entidad).__init__(self,name,port)
        self.sequenceNumberActual = 0
        print("Llegue a crear el cliente")
 
#para la subida

#PARA CLIENTE
    def enviarPaquete(self,mensaje):
        #modificamos para probar el server, pero se deberia mandar paquete
        #paquete = paquete(sequenceNumberActual, NOT_ACK, mensaje)
        #sequenceNumberActual += 1
        #self.clientSocket.sendto(paquete.encode(),(self.serverName,self.serverPort))
        #self.clientSocket.sendto(mensaje.encode('utf-8'),(self.serverName,self.serverPort))
        self.entidadSocket.sendto(str(mensaje).encode('utf-8'),(self.name,self.port))

    def enviarArchivo(self, ruta, enviador):
        file = enviador.abrirArchivo(ruta)
        enviador.enviarPaquete(file, self)


#para la descarga
    def recibirArchivo(self,ruta):
        #pensarla
        x = 1
    


