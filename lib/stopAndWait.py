#from asyncio.windows_events import NULL
from socket import *
import gestorPaquetes
import time
import enviador

MSJ_SIZE = 5
MAX_WAIT = 0.005
MAX_TRIES = 3

class StopAndWait(enviador.Enviador):

    def enviar(self,mensaje,entidad):
        pck = gestorPaquetes.crearPaquete(0,mensaje)
        pckBytes = gestorPaquetes.pasarPaqueteABytes(pck)
        entidad.enviarPaquete(pckBytes)
        verificar = gestorPaquetes.verificarACK(gestorPaquetes.pasarBytesAPaquete(pckBytes))
        return verificar

#STOP AND WAIT
    def enviarPaquete(self, file, entidad):

        mensaje = file.read(MSJ_SIZE)
        while(len(mensaje) > 0):
            timeout_start = time.time()
            #de mensaje a paquete
            verificar = self.enviar(mensaje,entidad)
            i = 0
            #chequear si llego un ack
            #si llego un ack, verificar que es el correcto
            #si no llego un ack o no es el correcto, -> reenvío
            #si salta el timer, -> reenvío
            #estoy dispuesta a reenviar MAX_TRIES
            while((verificar == False or time.time() >= timeout_start + MAX_WAIT) and i < MAX_TRIES):
                verificar = self.enviar(mensaje,entidad)
                timeout_start = time.time()
                i += 1

            mensaje = file.read(MSJ_SIZE)

        return 1 #despues revisamos qué devolver en cada caso de la función

"""
while((gestorPaquetes.verificar_paquete_ack(gestorPaquetes.formatearBytesAPaquete(pckBytes)) 
        or time.time() >= timeout_start + MAX_WAIT) and i < MAX_TRIES):
    paquete = gestorPaquetes.formatear(0,mensaje)
    pckBytes = gestorPaquetes.pasarPaqueteABytes(pck)
    entidad.enviarPaquete(paquete)
    timeout_start = time.time()
    i += 1
"""