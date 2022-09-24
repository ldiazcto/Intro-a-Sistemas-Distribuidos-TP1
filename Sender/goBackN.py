#from asyncio.windows_events import NULL
from socket import *
import time
import enviador

MSJ_SIZE = 35
MAX_WAIT = 0.005
MAX_TRIES = 3
MAX_VENTANA = 50

ERROR = -1
EXITO = 0

class goBackN(enviador.Enviador):
    def __init__(self):
        self.ackEsperado = 0
        self.paquetesEnVuelo = []
        self.timers = []

#Go back N
    def enviarPaquete(self, file):
        
#        try:
        for mensaje in iter(lambda: file.read(MSJ_SIZE),b''):
            
            if (len(self.paquetesEnVuelo) < MAX_VENTANA):
                self.paquetesEnVuelo.append(self.cliente.mandarPaquete(mensaje))
                cantidadEnVuelo+=1
                self.timers.append(time.time()) #Ordenado de mas viejo a mas nuevo
            
            
            esACK, ackRecibido = self.cliente.chequearSiLlegoACK()
            if (ackRecibido == self.ackEsperado):
                self.timers.pop(0) #Esto elimina el timer mas viejo
                self.paquetesEnVuelo = self.paquetesEnVuelo.filter(lambda pck: pck.sequenceNumber != self.ackEsperado)
                self.ackEsperado+=1
            
        
            #Si el timer sono o si el ack recibido no es el esperado, se envian todos los paquetes que estan en paquetesEnVuelo
            if ((time.time() >= self.timers[0] + MAX_WAIT) or (ackRecibido != self.ackEsperado)):
                    for pck in range(len(self.paquetesEnVuelo)):
                        self.cliente.mandarPaquete(pck.mensaje)

#        except file == NULL:
#            return ERROR
            
        return EXITO

        
