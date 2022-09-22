from asyncio.windows_events import NULL
from time import time as timer

NOT_ACK = -1

class Paquete:
    def __init__(self,sequenceNumber,ackNumber, mensaje):
        self.sequenceNumber = sequenceNumber
        self.ackNumber = ackNumber
        self.mensaje = mensaje

    def esACK(self):
        return (self.ackNumber != NOT_ACK)
        
def obtenerACK(self):
    if (self.esACK()):
        return self.ackNumber
    return NULL