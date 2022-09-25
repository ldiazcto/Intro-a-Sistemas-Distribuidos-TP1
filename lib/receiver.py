#from asyncio.windows_events import NULL
from socket import *
from abc import ABC, abstractclassmethod, abstractmethod
from os.path import exists
import sys

class Receiver(ABC):  
    #SI YA EXISTE EL ARCHIVO LO SOBRE ESCRIBO por que jodete usuario
    #no esta vacio

    def abrirArchivo(self,ruta):
        try:    
            if (exists(ruta)):
                file = open(ruta,'w')
                file.write("")
                close(file)    
            file = open(ruta,'a')
            return file
        except FileNotFoundError: #o IOERROR o FileExistsError
            print("FILE NO ENCONTRADO")
            sys.exit(2)
            
    def cerrarArchivo(self,file):
        try:
            file = close(file)

        except FileNotFoundError: #o IOERROR o FileExistsError
            print("FILE NO PUDO CERRAR")
            sys.exit(2)
        


    def guardarArchivo(self,file,mensaje):
        try:
            file.write(mensaje)

        except FileNotFoundError: #o IOERROR o FileExistsError
            print("FILE NO ENCONTRADO")
            sys.exit(2)


    @abstractmethod
    def enviarPaquete(self):
        pass
