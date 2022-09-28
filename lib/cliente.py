from socket import *
import entidad
import gestorPaquetes
import enviador
import select
import time
UPLOAD = 2
MAX_WAIT = 0.5

class Cliente(entidad.Entidad):
    
    def __init__(self, name, port):
        super(Cliente,self).__init__(name,port)
        self.gestorPaquetes = gestorPaquetes.Gestor_Paquete()
        print("Llegue a crear el cliente")
 
#para la subida

#PARA CLIENTE
    def enviarPaquete(self,pckBytes):
        self.entidadSocket.sendto(pckBytes ,(self.name,self.port))
        
    def enviarArchivo(self, file, enviador):
        enviador.enviarPaquete(file, self)


    def crearPaqueteHandshake(self, fileName, fileSize, operador):
        caracterSeparador = "-"
        caracterSeparadorBytes = bytes(caracterSeparador, 'ascii')
        fileNameBytes = bytes(fileName, 'ascii')
        fileSizeBytes = fileSize.to_bytes(2, 'big')

        mensaje = fileNameBytes
        if (operador == UPLOAD) :
            mensaje = mensaje + caracterSeparadorBytes + fileSizeBytes
        return self.gestorPaquetes.crearPaqueteHandshake(operador, mensaje)


    def enviarHandshake(self, fileName, fileSize, operador):
        paquete = self.crearPaqueteHandshake(fileName, fileSize, operador)
        paqueteBytes = gestorPaquetes.pasarPaqueteABytes(paquete)
        enviador.enviarPaqueteHandshake(self, paqueteBytes)
        

#para la descarga
    def recibirArchivo(self,ruta):
        #pensarla
        x = 1

    def recibirPaquete(self):
        timeout_start = time.time()
        while True:
            lista_sokcets_listos = select.select([self.entidadSocket], [], [], 1)
            if (time.time() >= (timeout_start + MAX_WAIT)):
                return self.gestorPaquetes.cierreConexion(5)
            if not lista_sokcets_listos[0]:
                continue
            paqueteString = self.entidadSocket.recvfrom(2048)
            return  self.gestorPaquetes.pasarBytesAPaquete(paqueteString)
        