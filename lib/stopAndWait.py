#from asyncio.windows_events import NULL
from socket import *
import time
import enviador

MSJ_SIZE = 5
MAX_WAIT = 0.5


class StopAndWait(enviador.Enviador):

    def enviar(self,mensaje,entidad):
        pck = self.gestorPaquetes.crearPaquete(mensaje)
        pckBytes = self.gestorPaquetes.pasarPaqueteABytes(pck)
        entidad.enviarPaquete(pckBytes)
        paqueteRecibido = entidad.recibirPaquete()
        cantidad_intentos = 1
        while(paqueteRecibido == None and cantidad_intentos <= 3):
            entidad.enviarPaquete(pckBytes)
            paqueteRecibido = entidad.recibirPaquete()
            #print("Entro a recibirPaquete(): ",cantidad_intentos)
            cantidad_intentos += 1
        if(cantidad_intentos > 3):
            return (False,None)
        return (True,paqueteRecibido)

#STOP AND WAIT
    def enviarPaquete(self, file, entidad):

        mensaje = file.read(MSJ_SIZE)
        
        while(len(mensaje) > 0):
            print("mensaje: ",mensaje)
            #de mensaje a paquete
            intentar_mandar,paquete_recibido = self.enviar(mensaje,entidad)
            #chequear si llego un ack
            #si llego un ack, verificar que es el correcto
            #si no llego un ack o no es el correcto, -> reenvío
            #si salta el timer, -> reenvío
            #estoy dispuesta a reenviar MAX_TRIES
            
            if (intentar_mandar == False):
                return
            verificar_ack = self.gestorPaquetes.verificarACK(paquete_recibido)
            intentar_mandar_ack = True
            if(verificar_ack == False): #EXTREMA SEGURIDAD --> ACK CORRUPTO
                cant_max_envios = 0
                while (cant_max_envios <= 3):
                    intentar_mandar_ack,paquete_recibido = self.enviar(mensaje,entidad)
                    cant_max_envios += 1
            if (intentar_mandar_ack == False):
                return
            """
            i = 1
            while(verificar_ack == False and i <= 3):
                print("-- ENVIAR PAQUETE --- No recibí el ACK o salto el timer, envío de nuevo. Vez ",i," de 4")
                verificar,paquete_perdido = self.enviar(mensaje,entidad)
                i += 1
            """
            
            mensaje = file.read(MSJ_SIZE)
        return
       

"""
while((gestorPaquetes.verificar_paquete_ack(gestorPaquetes.formatearBytesAPaquete(pckBytes)) 
        or time.time() >= timeout_start + MAX_WAIT) and i < MAX_TRIES):
    paquete = gestorPaquetes.formatear(0,mensaje)
    pckBytes = gestorPaquetes.pasarPaqueteABytes(pck)
    entidad.enviarPaquete(paquete)
    timeout_start = time.time()
    i += 1
"""