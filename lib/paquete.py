#from asyncio.windows_events import NULL
import string
from time import time as timer

DATA = 0 #a veces llamado NOT_ACK
ACK = 1
UPLOAD = 2
DOWNLOAD = 3
REFUSED = 4
FIN = 5

class Paquete:
    def __init__(self,sequenceNumber,operador, mensaje):
        self.sequenceNumber = sequenceNumber
        self.operador = operador
        self.mensaje = mensaje

    def esACK(self):
        if self.operador == ACK:
            return True
        return False
    
    def obtenerOperador(self):
        return self.operador

    def obtenerSeqNumber(self):
        return self.sequenceNumber

    def obtenerMensaje(self):
        return self.mensaje

    def esUpload(self):
        return self.operador == UPLOAD

    def esDownload(self):
        return self.operador == DOWNLOAD

    def esRefused(self):
        return self.operador == REFUSED

    def esFin(self):
        return self.operador == FIN