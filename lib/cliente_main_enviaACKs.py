#main para pruebas de cliente recibiendo paquetes con info

import os
from socket import AF_INET, SOCK_DGRAM
import cliente
import sys


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
    file_handler = logging.FileHandler(filename='tmp.log')
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    handlers = [file_handler, stdout_handler]

    logging.basicConfig(
        level=logging.DEBUG, 
        format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
        handlers=handlers
    )
    
    logger = logging.getLogger()
    
    logger.info("Se inicio el logger")   
    cliente_prueba = cliente.Cliente(receiverName, receiverPort)
    cliente_prueba.entidadSocket.bind((receiverName,receiverPort)) #el cliente escucha el serverPort y serverName del server

    
    print("Se creo el cliente con exito")
    
    #recibo con mi función y genero el archivo

    file = cliente_prueba.recibirArchivo("/Users/abrildiazmiguez/Desktop", "archivoDelCliente.txt")
    cerrarArchivo(file)
    cliente_prueba.entidadSocket.close()
    return 0



main()