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

            #Si en mi primer envio en la ventana N, recibo acks, osea ok el envio, sigo leyendo y reinicio la lista en vuelo
            if(verificar == True and len(self.paquetesEnVuelo) > MAX_VENTANA):
                self.paquetesEnVuelo = []

        return 1


"""
#--------------

    def recibirAcks(listaAcks):
        for i in range(len(listaAcks)):
            if listaAcks[i] == False:
                return i, False
        #Me va adevolver la posición desde el correcto ack recibido
        return 0, True

        
    def enviarPaquete(self, file, entidad):

        mensaje = file.read(MSJ_SIZE)
        listaAcks = []
        while len(mensaje) > 0 :
            
            if (len(self.paquetesEnVuelo) < MAX_VENTANA):

                verificar = self.enviar(mensaje,entidad)
                self.timers.append(time.time()) #Ordenado de mas viejo a mas nuevo
                listaAcks.append(verificar)

            else:
                posReenvio, recepcion = self.recibirAcks(listaAcks)
            #Hasta aca suponiendo que se cumplio el envio de la primera tanda
            #Tengo la posicion desde el paquete que no recibi el ack, por lo que me tocaria retransmitir de ahi
            #Timeout (?) 

            #el temporizador debe estar corriendo en cada tanda de mi ventana N, y reiniciar en la prox
            #Si termina, tambien vuelvo a reenviar
            if(recepcion == False or self.timers[0] + MAX_WAIT < time.time()):
                for pck in range(len(self.paquetesEnVuelo) - posReenvio):
                    verificar = self.enviar(self.paquetesEnVuelo[posReenvio + pck].obtenerMensaje(),entidad)
                    self.timers.append(time.time())
            
            mensaje = file.read(MSJ_SIZE)

            #Si en mi primer envio en la ventana N, recibo acks, osea ok el envio, sigo leyendo y reinicio la lista en vuelo
            if(verificar == True and len(self.paquetesEnVuelo) > MAX_VENTANA):
                self.paquetesEnVuelo = []

        return 1
"""
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

        
