#from asyncio.windows_events import NULL
from socket import *
from abc import ABC, abstractclassmethod, abstractmethod
import sys
import gestorPaquetes
import time

MAX_WAIT = 0.005
MAX_TRIES = 3

class Enviador(ABC):  

    def __init__(self):
        self.gestorPaquetes = gestorPaquetes.Gestor_Paquete()
    
    #no la probé
    def enviarPaqueteHandshake(self, cliente, paqueteBytes):
        cliente.enviarPaquete(paqueteBytes)
        timeout_start = time.time()
        i = 0
        recepcionACKCorrecto = False  
        while (i < MAX_TRIES and not recepcionACKCorrecto) :
            paqueteRecibido = cliente.recibirPaquete()
            recepcionACKCorrecto = self.gestorPaquetes.verificarACK(paqueteRecibido)
            if (not recepcionACKCorrecto or time.time() > timeout_start + MAX_WAIT) :
                cliente.enviarPaquete(paqueteBytes)
                timeout_start = time.time()
                i += 1


    @abstractmethod
    def enviar(self,mensaje,entidad):
        pass
    @abstractmethod
    def enviarPaquete(self):
        pass
