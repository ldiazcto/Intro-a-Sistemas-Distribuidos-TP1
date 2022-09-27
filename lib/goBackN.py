#from asyncio.windows_events import NULL
from socket import *
import time
import enviador
import gestorPaquetes

MSJ_SIZE = 5
MAX_WAIT = 0.0005
MAX_TRIES = 3
MAX_VENTANA = 10

class GoBackN(enviador.Enviador):

    def __init__(self):
        self.paquetesEnVuelo = []
        self.timers = []

    def enviar(self,mensaje,entidad):
        pck = gestorPaquetes.crearPaquete(0,mensaje)
        pckBytes = gestorPaquetes.pasarPaqueteABytes(pck)
        entidad.enviarPaquete(pckBytes)
        self.paquetesEnVuelo.append(gestorPaquetes.pasarBytesAPaquete(pckBytes))
        verificar = gestorPaquetes.verificarACK(gestorPaquetes.pasarBytesAPaquete(pckBytes))
        return verificar
#Go back N
    def enviarPaquete(self, file, entidad):

        mensaje = file.read(MSJ_SIZE)
        while len(mensaje) > 0 :
            
            if (len(self.paquetesEnVuelo) < MAX_VENTANA):

                verificar = self.enviar(mensaje,entidad)
                self.timers.append(time.time()) #Ordenado de mas viejo a mas nuevo

            if(verificar == False or self.timers[0] + MAX_WAIT < time.time()):
                for pck in range(len(self.paquetesEnVuelo)):
                    verificar = self.enviar(self.paquetesEnVuelo[pck].obtenerMensaje(),entidad) 
                    self.timers.append(time.time())
            #retransmision de paquetes desde el ultimo ack recibido
            
            mensaje = file.read(MSJ_SIZE)

        return 1

"""
if (self.timers[0] + MAX_WAIT < time.time() ) :
    self.timers = []
    for msj in range(len(self.paquetesEnVuelo)):
        #entidad.enviarPaquete(pck.mensaje)
        self.paquetesEnVuelo = self.enviar(mensaje,entidad)
        self.timers.append(time.time())
"""
#esACK, ackRecibido = self.entidad.chequearSiLlegoACK()
#if (ackRecibido == self.ackEsperado):
#    self.timers.pop(0) #Esto elimina el timer mas viejo
#    self.paquetesEnVuelo = self.paquetesEnVuelo.filter(lambda pck: pck.sequenceNumber != self.ackEsperado)
#    self.ackEsperado+=1

        
