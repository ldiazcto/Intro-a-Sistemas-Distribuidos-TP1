from socket import *
import entidad
import gestorPaquetes
import enviador
import select
import time
import os
import logging
#import cliente_main

UPLOAD = 2
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
    def enviarPaquete(self,pckBytes):
        self.entidadSocket.sendto(pckBytes ,(self.name,self.port))
        #print("-- ENVIAR PAQUETE -- envié el paquete actual")
        
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


    def entablarHandshake(self, fileName, fileSize, operador):
        paquete = self.crearPaqueteHandshake(fileName, fileSize, operador)
        paqueteBytes = self.gestorPaquetes.pasarPaqueteABytes(paquete)
        self.enviador.enviarPaqueteHandshake(self, paqueteBytes)
        funciono = False  #ME FALTA VERIFICAR QUE HAYA FUNCIONADO! verifica el ack que debí haber recibido  -- no sé si recibirPaquete sirve para esto
        if funciono :
            return True
        else :
            return False

    #para la descarga
    def recibirArchivo(self, filePath, fileName):
        # hago el handshake para download -> hecho en el main
        # si recibo el ack del handshake -> continúo (hecho en el main)
        
        ruta = filePath + "/" + fileName
        file = open(ruta, 'w')
        
        i = 0
        timeActual = time.time()
        self.entidadSocket.setblocking(NOT_BLOCKING)
        while True:
            print("\n--NUEVA ITERACIÓN DEL WHILE --")
            try :
                paqueteBytes, serverAdress = self.entidadSocket.recvfrom(2048)
            except BlockingIOError:
                if time.time() > timeActual + MAX_WAIT_RESPONSE :
                    break
                continue
            print("Recibí algo! :) ")

            print("Y es un paquete :D ")
            paqueteRecibido = self.gestorPaquetes.pasarBytesAPaquete(paqueteBytes)
            esPaqueteOrdenado = self.gestorPaquetes.verificar_mensaje_recibido(paqueteRecibido)
            if (esPaqueteOrdenado) :
                ("\nEs un paquete ordenado\n")
                paqueteACK = self.gestorPaquetes.crearPaqueteACK(ACK_CORRECT)
            
                nombre, extension = fileName.split('.')
                mensaje = paqueteRecibido.obtenerMensaje()
                if (extension == "txt" or extension == "docs" ) :
                    mensaje = mensaje.decode('ascii')
                
                file.write(mensaje) #no sé si estoy escribiendo en ascii o bytes
                timeActual = time.time()
                i = 0
            
            else :
                paqueteACK = self.gestorPaquetes.crearPaqueteACK(ACK_INCORRECT)
                i += 1

            paqueteACKBytes = self.gestorPaquetes.pasarPaqueteABytes(paqueteACK)
            
            #envio el paquete de ack
            self.enviarPaquete(paqueteACKBytes)
            if (paqueteRecibido.esFin()) :
                print("ES DE TIPO FIN!")
            else:
                print("NO es de tipo fin")
            if not (i <= MAX_TRIES and not paqueteRecibido.esFin()) :
                break
                #es feo, sí, pero estoy emulando un do-while. Esto quiere decir que quiero que se ejecute el loop hasta que 
                #           el server me envió un paquete de fin  o
                #           haya esperado el mismo paquete la máxima cantidad de veces (?)
            
        self.entidadSocket.setblocking(BLOCKING)

        if (i >= MAX_TRIES or time.time() > timeActual + MAX_WAIT_RESPONSE) :
            file.close()
            os.remove(file.name)
            print("Salto el timer o recibí más de tres veces el paquete en desorden")
            return None
            #acá debería borrar el archivo hecho porque el servidor no responde y no me mandó el FIN
        
        print("tengo el archivo y no hubo ningun error, bien!")
        return file


    def recibirPaquete(self):
        timeout_start = time.time()
        while True:
            lista_sockets_listos = select.select([self.entidadSocket], [], [], 1)
            var = time.time()
            if (var >= (timeout_start + MAX_WAIT)):   
                return None
                #volver a mandar_mensaje
            if not lista_sockets_listos[0]:
                continue
            paqueteString, server_address = self.entidadSocket.recvfrom(2048)
            return self.gestorPaquetes.pasarBytesAPaquete(paqueteString)
        