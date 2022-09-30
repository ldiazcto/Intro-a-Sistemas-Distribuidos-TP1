import os
import cliente, stopAndWait, goBackN
import gestorPaquetes
import getopt
import sys
import logging

UPLOAD = 2

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
        
        resultado = cliente_prueba.entablarHandshake("hola.txt", 1, UPLOAD)
        print("\n -- Volvi al iniciaHandshakeUPLOAD --")
        if resultado:
                print("Cliente: el entablarHandshake funciono correctamente, wii")
        else:
                print("Cliente: el entablarHandshake no funciono, algo salio mal :(")


        cliente_prueba.entidadSocket.close()
        return 0


def iniciaHandshakeDOWNLOAD():
        print("Aun no implementado :)")


print("\n--PRUEBA CLIENTE INICIA HANDSHAKE UPLOAD--")
iniciaHandshakeUPLOAD()

print("\n\n--PRUEBA CLIENTE RECIBE HANDSHAKE DOWNLOAD--")
iniciaHandshakeDOWNLOAD()
