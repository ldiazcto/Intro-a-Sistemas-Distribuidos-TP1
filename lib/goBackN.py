#from asyncio.windows_events import NULL
from socket import *
import time
import enviador
import paquete
import goBackNRecv

MSJ_SIZE = 5
MAX_WAIT = 0.0005
MAX_TRIES = 3
MAX_VENTANA = 10

class GoBackN(enviador.Enviador):

    def __init__(self):
        self.paquetesEnVuelo = []
        self.timers = []
        self.goBackNRecv = goBackNRecv.GoBackNRecv(MAX_VENTANA)
        super(GoBackN, self).__init__()

    def agregarPaqueteEnVuelo(self,paquete):
        self.paquetesEnVuelo.append(self.gestorPaquetes.pasarBytesAPaquete(paquete))

    def paqueteEnVueloI(self,i):
        return(self.paquetesEnVuelo[i])
    
    def agregarTimer(self,timer):
        self.timers.append(time.time())

    def timerI(self,i):
        return(self.timers[i])

    def enviar(self,mensaje,entidad):
        pck = self.gestorPaquetes.crearPaquete(mensaje)
        pckBytes = self.gestorPaquetes.pasarPaqueteABytes(pck)
        entidad.enviarPaquete(pckBytes)
        self.paquetesEnVuelo.append(self.gestorPaquetes.pasarBytesAPaquete(pckBytes))
        """
        paqueteRecibido = entidad.recibirPaquete()
        if (paqueteRecibido == None):
            return False
        verificar = self.gestorPaquetes.verificarACK(paqueteRecibido)
        return verificar
        """
#Go back N
    def enviarPaquete(self, file, entidad):

        mensaje = file.read(MSJ_SIZE)
        while (len(mensaje) > 0):
            if (len(self.paquetesEnVuelo) < MAX_VENTANA):
                self.enviar(mensaje,entidad) #este seria solo enviar
                self.timers.append(time.time()) #Ordenado de mas viejo a mas nuevo
            self.goBackNRecv.recibirParalelo(self,entidad,self.paquetesEnVuelo)
            mensaje = file.read(MSJ_SIZE)
        
        return 1


    """while (termino de leer el archivo):
        mensaje =  leer
        if tamaño actual ventana < max ventana:
            mando el mensaje
        si el timer esta prendido:
            no hago nada
        empiezo timer
        recibo ack pero es no bloqueante
"""

"""
base_envio = 0
paquete_a_enviar = 0

mensaje = file.read(MSJ_SIZE)
while len(mensaje) > 0:
    if(paquete_a_enviar < base_envio + MAX_VENTANA):
        self.enviar(mensaje,entidad)
        paquete_a_enviar += 1
    paqueteRecibido = entidad.recibirPaquete()
    verificar = goBackN.gestorPaquetes.verificarACK(paqueteRecibido)
    if(verificar == True):
        base_envio += 1
        if(paqueteRecibido in paquetesEnVuelo):
            paquetesEnVuelo.remove(paqueteRecibido)
        if(base_envio == paquete_a_enviar):
            timeout = 0
        else:
            timeout = time.time()

    if(timeout):
        timeout = time.time()
        for(pck in paquetesEnVuelo):
            self.enviar(pck.obtenerMensaje(),entidad)
    mensaje = file.read(MSJ_SIZE)
    
"""

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

        
