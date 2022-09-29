import time
from socket import*
import goBackN
import threading
import entidad

MAX_WAIT = 0.0005

class GoBackNRecv(threading.Thread,entidad.Entidad):
    def __init__(self):
        threading.Thread.__init__(self)
        entidad.Entidad.__init__(self,'',12000)


    def recivirParalelo(self,goBackN,entidad):
        paqueteRecibido = entidad.recibirPaquete()
        if (paqueteRecibido == None):
            return False
        verificar = goBackN.gestorPaquetes.verificarACK(paqueteRecibido)
        
        if(verificar == False or goBackN.timersI[0] + MAX_WAIT < time.time()):
            for pck in range(len(goBackN.paquetesEnVuelo)):
                verificar = goBackN.enviar(goBackN.paquetesEnVueloI[pck].obtenerMensaje(),entidad) 
                goBackN.agregarTimer(time.time())
                #retransmision de paquetes desde el ultimo ack recibido