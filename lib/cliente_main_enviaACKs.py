#main para pruebas de cliente recibiendo paquetes con info

import os
from socket import AF_INET, SOCK_DGRAM
import cliente
import sys


def abrirArchivo(ruta):
        try:
            file = open(ruta,'rb')
            return file
        except FileNotFoundError: #o IOERROR o FileExistsError
            print("FILE NO ENCONTRADO")
            sys.exit(2)

def cerrarArchivo(file):
    if (file is not None) :
        file.close()

#no tiene la info, la recibe

def main():
   
    #creo cliente
    #llamo a recibir archiv y forzar que reciba las cosas, sin server de por medio
    #generar un archivo nuestro y mandárselo al socket que el cliente escucha
   
    receiverPort = 12000
    receiverName = "localhost"
    
    cliente_prueba = cliente.Cliente(receiverName, receiverPort)
    cliente_prueba.entidadSocket.bind((receiverName,receiverPort)) #el cliente escucha el serverPort y serverName del server

    
    print("Se creo el cliente con exito")
    
    #recibo con mi función y genero el archivo

    file = cliente_prueba.recibirArchivo("/Users/abrildiazmiguez/Desktop", "archivoDelCliente.txt")
    cerrarArchivo(file)
    cliente_prueba.entidadSocket.close()
    return 0



main()