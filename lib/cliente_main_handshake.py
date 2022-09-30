import os
import cliente, stopAndWait, goBackN
import gestorPaquetes
import getopt
import sys
import logging

UPLOAD = 2
DOWNLOAD = 3

def cerrarArchivo(file):
    if (file is not None) :
        file.close()

#envía el handshake

def iniciaHandshakeUPLOAD():
   
        #creo cliente
        #como estoy en upload, creo paquete de handshake
        #se lo envío al server llamando a cliente.entablarHandshake()
        #si funciona devuelve True, es porque el paquete se envió al server, el server lo recibió y se recibió un ack de respuesta

        receiverPort = 12000
        receiverName = "localhost"
        
        cliente_prueba = cliente.Cliente(receiverName, receiverPort)
        print("Se creo el cliente con exito")
        
        resultado = cliente_prueba.entablarHandshake("hola.txt", 395, UPLOAD)
        print("\n -- Volvi al iniciaHandshakeUPLOAD --")
        if resultado:
                print("Cliente: el entablarHandshake funciono correctamente, wii")
        else:
                print("Cliente: el entablarHandshake no funciono, algo salio mal :(")


        cliente_prueba.entidadSocket.close()
        return 0


def downloadArchivoInexistente():
   
        receiverPort = 12000
        receiverName = "localhost"
        
        cliente_prueba = cliente.Cliente(receiverName, receiverPort)
        print("Se creo el cliente con exito")
        
        resultado = cliente_prueba.entablarHandshake("hola.txt", 395, DOWNLOAD)
        print("\n -- Volvi al iniciaHandshakeDOWNLOAD --")
        if resultado:
                print("No debería caer acá, estoy intentando descargar un archivo inexistente")
        else:
                print("El archivo a descargar no existe, debería caer acá")
                

        cliente_prueba.entidadSocket.close()
        return 0


def downloadArchivoExistente():
   
        receiverPort = 12000
        receiverName = "localhost"
        
        cliente_prueba = cliente.Cliente(receiverName, receiverPort)
        print("Se creo el cliente con exito")
        
        resultado = cliente_prueba.entablarHandshake("prueba_doc.doc", 395, DOWNLOAD)
        print("\n -- Volvi al iniciaHandshakeDOWNLOAD --")
        if resultado:
                print("debería caer acá, el archivo existe")
        else:
                print("NO DEBERÍA CAER ACÁ")
                

        cliente_prueba.entidadSocket.close()
        return 0


print("\n--PRUEBA CLIENTE INICIA HANDSHAKE UPLOAD--")
iniciaHandshakeUPLOAD()

print("\n\n--PRUEBA CLIENTE RECIBE HANDSHAKE DOWNLOAD--")
downloadArchivoInexistente()
downloadArchivoExistente()
