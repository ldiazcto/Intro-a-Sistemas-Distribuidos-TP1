#from asyncio.windows_events import NULL
from socket import *
import time
import enviador

MSJ_SIZE = 5
MAX_WAIT = 1


class StopAndWait(enviador.Enviador):

    def enviar(self,mensaje,entidad):
        pck = self.gestorPaquetes.crearPaquete(mensaje)
        pckBytes = self.gestorPaquetes.pasarPaqueteABytes(pck)
        entidad.enviarPaquete(pckBytes)
        cantidad_intentos = 1
        print("\n--El mensaje a enviar es: ", mensaje)
        print("\n-cantidad intentos es ", cantidad_intentos)

        paqueteRecibido = entidad.recibirPaquete()
        
        while(paqueteRecibido == None and cantidad_intentos <= 3):
            print("\n\n El paquete recibido es de tipo ", paqueteRecibido)
            entidad.enviarPaquete(pckBytes)
            paqueteRecibido = entidad.recibirPaquete()
            cantidad_intentos += 1
            print("\n--El mensaje a enviar es: ", mensaje)
            print("\n-cantidad intentos es ", cantidad_intentos)
        if(cantidad_intentos > 3):
            return (False,None)
        return (True,paqueteRecibido)

#STOP AND WAIT
    def enviarPaquete(self, file, entidad):

        mensaje = file.read(MSJ_SIZE)
        
        while(len(mensaje) > 0):
            #de mensaje a paquete
            intentar_mandar,paquete_recibido = self.enviar(mensaje,entidad)
            #chequear si llego un ack
            #si llego un ack, verificar que es el correcto
            #si no llego un ack o no es el correcto, -> reenvío
            #si salta el timer, -> reenvío
            #estoy dispuesta a reenviar MAX_TRIES
            
            if (intentar_mandar == False):
                print(" \n intentar mandar es False, return ")
                return
            verificar_ack = self.gestorPaquetes.actualizarACK(paquete_recibido) #lo cambi;e a verificarACK
            intentar_mandar_ack = True
            if(verificar_ack == False): #EXTREMA SEGURIDAD --> ACK CORRUPTO
                cant_max_envios = 0
                while (cant_max_envios <= 3):
                    intentar_mandar_ack,paquete_recibido = self.enviar(mensaje,entidad)
                    cant_max_envios += 1
            if (intentar_mandar_ack == False):
                print ("\n intentar mandar ack es False, return")
                return
            mensaje = file.read(MSJ_SIZE)
        return
       