#from asyncio.windows_events import NULL
from socket import *
import time
import enviador

MSJ_SIZE = 5
MAX_WAIT = 0.0005
MAX_TRIES = 3
MAX_VENTANA = 10

class GoBackN(enviador.Enviador):

    def __init__(self):
        self.ackEsperado = 0
        self.paquetesEnVuelo = []
        self.timers = []

#Go back N
    def enviarPaquete(self, file, entidad):

        mensaje = file.read(MSJ_SIZE)
        while len(mensaje) > 0 :
            
            if (len(self.paquetesEnVuelo) < MAX_VENTANA):
                entidad.enviarPaquete(mensaje)
                self.paquetesEnVuelo.append(mensaje)
                self.timers.append(time.time()) #Ordenado de mas viejo a mas nuevo
            
            #esACK, ackRecibido = self.entidad.chequearSiLlegoACK()
            #if (ackRecibido == self.ackEsperado):
            #    self.timers.pop(0) #Esto elimina el timer mas viejo
            #    self.paquetesEnVuelo = self.paquetesEnVuelo.filter(lambda pck: pck.sequenceNumber != self.ackEsperado)
            #    self.ackEsperado+=1
            
            if (self.timers[0] + MAX_WAIT < time.time() ) :
                self.timers = []
                for msj in range(len(self.paquetesEnVuelo)):
                    #entidad.enviarPaquete(pck.mensaje)
                    entidad.enviarPaquete(self.paquetesEnVuelo[msj])
                    self.timers.append(time.time())

            
            mensaje = file.read(MSJ_SIZE)


        return 1

        
