import time
from socket import*
import threading
import entidad

MAX_WAIT = 0.0005

class GoBackNRecv(threading.Thread):
    def __init__(self,ventana):
        threading.Thread.__init__(self)
        self.activo = True
        self.cantidad_ack_recibidas = 0
        self.maxVentana = ventana

    def recibirParalelo(self,goBackN,entidad,paquetesEnVuelo):
        #while(self.activo and not paqueteRecibido.esFin()):
        paqueteRecibido = entidad.recibirPaquete()
        if (paqueteRecibido == None):
            return False
        #if(paqueteRecibido.esFin()):
         #   return 
        verificar = goBackN.gestorPaquetes.verificarACK(paqueteRecibido)

        if (verificar == True):
            self.cantidad_ack_recibidas += 1
            if(paqueteRecibido in paquetesEnVuelo):
                paquetesEnVuelo.remove(paqueteRecibido)
            self.maxVentana += self.cantidad_ack_recibidas
            
        if(verificar == False or goBackN.timerI(0) + MAX_WAIT < time.time()):
            for pck in range(len(paquetesEnVuelo)):
                verificar = goBackN.enviar(goBackN.paqueteEnVueloI(pck).obtenerMensaje(),entidad) 
                goBackN.agregarTimer(time.time())
                #retransmision de paquetes desde el ultimo ack recibido
        return

        