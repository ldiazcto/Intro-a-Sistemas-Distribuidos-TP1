#from asyncio.windows_events import NULL
from time import time as timer

NOT_ACK = 0

class Paquete:
    def __init__(self,sequenceNumber,esACK, mensaje):
        self.sequenceNumber = sequenceNumber
        self.esACK = esACK
        self.mensaje = mensaje

    def esACK(self):
        if self.esACK == NOT_ACK:
            return False
        return True
        
    def obtenerACK(self):
        if (self.esACK()):
            return self.ackNumber
        return 0

    def obtenerSeqNumber(self):
        return self.sequenceNumber

    def obtenerMensaje(self):
        return self.mensaje