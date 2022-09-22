from asyncio.windows_events import NULL
from socket import *
from abc import ABC, abstractclassmethod, abstractmethod

class Enviador(ABC):

    def __init__(self, cliente):
        cliente = cliente
        stopAndWait = stopAndWait()
        goBackN = goBackN()
        

    def leerArchivo(ruta):
        try:
            file = open(ruta,"r")
        except FileNotFoundError: #o IOERROR o FileExistsError
            return NULL
        return file

    @abstractmethod
    def enviarPaquete(self):
        pass
