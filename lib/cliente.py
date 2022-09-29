from socket import *
import entidad
import gestorPaquetes
import time
import os
import logging
#import cliente_main

MAX_WAIT = 0.5
MAX_TRIES = 2
ACK_INCORRECT = 0
ACK_CORRECT = 1
MAX_WAIT_RESPONSE = 300
NOT_BLOCKING = 0
BLOCKING = 1

class Cliente(entidad.Entidad):
    
    def __init__(self, name, port):
        super(Cliente,self).__init__(name,port)
        self.gestorPaquetes = gestorPaquetes.Gestor_Paquete()
        #logger.info("Llegue al cliente")
 
#para la subida

#PARA CLIENTE
       
    def enviarArchivo(self, file, enviador):
        enviador.enviarPaquete(file, self)


    def prepararMensajeParaArchivo(fileName, paqueteRecibido):
        nombre, extension = fileName.split('.')
        mensaje = paqueteRecibido.obtenerMensaje()
        if (extension == "txt" or extension == "docs" ) :
            mensaje = mensaje.decode('ascii')
        return mensaje

    #para la descarga
    def recibirArchivo(self, filePath, fileName):
        ruta = filePath + "/" + fileName
        file = open(ruta, 'w')
        
        i = 0
        timeActual = time.time()
        self.entidadSocket.setblocking(NOT_BLOCKING)
        while True:
            try :
                paqueteBytes, serverAdress = self.entidadSocket.recvfrom(2048)
            except BlockingIOError:
                if time.time() > timeActual + MAX_WAIT_RESPONSE :
                    break
                continue

            paqueteRecibido = self.gestorPaquetes.pasarBytesAPaquete(paqueteBytes)
            esPaqueteOrdenado = self.gestorPaquetes.verificar_mensaje_recibido(paqueteRecibido)
            if (esPaqueteOrdenado) :
                paqueteACK = self.gestorPaquetes.crearPaqueteACK(ACK_CORRECT)
                mensaje = self.prepararMensajeParaArchivo(fileName, paqueteRecibido)
                
                file.write(mensaje)
                timeActual = time.time()
                i = 0
            
            else :
                paqueteACK = self.gestorPaquetes.crearPaqueteACK(ACK_INCORRECT)
                i += 1

            paqueteACKBytes = self.gestorPaquetes.pasarPaqueteABytes(paqueteACK)
            
            self.enviarPaquete(paqueteACKBytes)
            if not (i <= MAX_TRIES and not paqueteRecibido.esFin()) :
                break
                #es feo, sí, pero estoy emulando un do-while. Esto quiere decir que quiero que se ejecute el loop hasta que 
                #           el server me envíe un paquete de fin  o
                #           haya recibido el mismo paquete mal tres veces
            
        self.entidadSocket.setblocking(BLOCKING)

        if (i >= MAX_TRIES or time.time() > timeActual + MAX_WAIT_RESPONSE) :
            file.close()
            os.remove(file.name)
            return None
        
        return file
        