#from asyncio.windows_events import NULL
from socket import *
from abc import ABC, abstractclassmethod, abstractmethod
import sys

class Enviador(ABC):

    # def __init__(self, cliente):
    #     cliente = cliente
        #stopAndWait = stopAndWait()
        #goBackN = goBackN()
        

    def abrirArchivo(self,ruta):
        try:
            file = open(ruta,'r')
            return file
        except FileNotFoundError: #o IOERROR o FileExistsError
            print("FILE NO ENCONTRADO")
            sys.exit(2)
        

    @abstractmethod
    def enviarPaquete(self):
        pass
