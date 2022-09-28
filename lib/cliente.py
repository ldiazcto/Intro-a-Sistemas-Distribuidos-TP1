from socket import *
import entidad
import gestorPaquetes

NOT_ACK = 0

class Cliente(entidad.Entidad):
    
    def __init__(self, name, port):
        super(Cliente, self).__init__(name,port)
        print("Llegue a crear el cliente")
 
#para la subida

#PARA CLIENTE
    def enviarPaquete(self,pckBytes):
        self.entidadSocket.sendto(pckBytes ,(self.name,self.port))
        
    def enviarArchivo(self, ruta, enviador):
        file = enviador.abrirArchivo(ruta)
        enviador.enviarPaquete(file, self)


#para la descarga
    def recibirArchivo(self,ruta):
        #pensarla
        x = 1

    def recibirPaquete(self):
        paqueteString = self.entidadSocket.recvfrom(2048)
        return  gestorPaquetes.formatearBytesAPaquete(paqueteString)
        