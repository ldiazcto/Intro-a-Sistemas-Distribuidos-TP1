from socket import *
import time
import enviador
import paquete

MSJ_SIZE = 150
N = 100 #tamanio de la ventana
MAX_WAIT_GOBACKN = 30
MAX_TRIES = 3
MAX_WAIT_ACKS = 5

class GoBackN(enviador.Enviador):

    # GO BACK N TIENE ACK ACUMULATIVOS, SI SE PIERDE UN PAQUETE ME VA A DEVOLVER EL ACK DEL ANTERIOR YA QUE VA A DESCARTAR LOS PAQUETES SIGUIENTES AL QUE PERDIO

    def __init__(self):
        self.older_seq_number = 0
        self.new_seq_number = 0
        self.paquetesEnVuelo = []
        super(GoBackN,self).__init__()

    def enviar(self,mensaje,entidad):
        return 1


    def recibirPaqueteACK(self, entidad) :
        pckRecibido = entidad.recibirPaqueteBackN() #obtengo el ultimo paquete recibido
        ackRecibido = self.gestorPaquetes.actualizarACK(pckRecibido)
        return pckRecibido, ackRecibido


    def enviarPaquete(self,file,entidad):
        mensaje = file.read(MSJ_SIZE)
        timeout_start = 0
        while (len(mensaje) > 0):
            
            #si el numero de sequencia del siguiente paquete a enviar es menor al numero de seq del primer paquete que envie
            # -- ENVIAR ACK --
            if(self.new_seq_number < self.older_seq_number + N):
                if(self.older_seq_number == self.new_seq_number): #entrás cuando corriste la ventana entera
                    timeout_start = time.time()         
                pck = self.gestorPaquetes.crearPaquete(mensaje)
                self.paquetesEnVuelo.append(pck)
                entidad.enviarPaquete(self.gestorPaquetes.pasarPaqueteABytes(pck))
                self.new_seq_number = pck.obtenerSeqNumber()
            
            # -- Espero un poquito de tiempo, porque los paquetes son lentos -- 
            timerEsperaACKs = time.time()
            esACKEsperado= False
            pckRecibido = None
            while(time.time() < timerEsperaACKs + MAX_WAIT_ACKS) and esACKEsperado == False:
                pckRecibido, esACKEsperado = self.recibirPaqueteACK(entidad)
                #agrego esta línea porque antes de continuar intentando enviar, sí o sí me tiene que haber llegado algo
        
            
            # -- VERIFICACION DE ACK --
            if (esACKEsperado) : #SI RECIBO UN ACK, SIGNIFICA QUE RECIBI EL ACK DEL ULTIMO PAQUETE QUE LLEGO BIEN
                                        # (ES DECIR QUE, TODOS LOS PAQUETES ANTERIORES TMB LLEGARON BIEN)
                #muevo el older_seq_number a la posicion siguiente al new_seq_number
                self.older_seq_number = pckRecibido.obtenerSeqNumber()+1 
                timeout_start = time.time() #reinicio el timer porque los paquetes me llegaron bien, corro el older porque tengo que mandar paquetes nuevos 
                self.paquetesEnVuelo.pop(0) #borro el paquete que llego bien (voy borrando de a uno)
                    

            # -- REENVIAR PCKS EN CASO DE ERROR --
            saltoTimerReenvio = (time.time() - timeout_start)  >= MAX_WAIT_GOBACKN
            if(esACKEsperado == False and  saltoTimerReenvio): #SI SALTO TIMEOUT, ENTONCES PERDI UN PAQUETE Y POR ENDE TENGO 
                                                            #QUE VOLVER A INICIAR EL TIMER Y ENVIAR LOS PAQUETES QUE ME QUEDARON EN LA LISTA DE PAQUETES EN VUELO
                timeout_start = time.time()
                for pck in range(len(self.paquetesEnVuelo)):
                    entidad.enviarPaquete(self.gestorPaquetes.pasarPaqueteABytes(self.paquetesEnVuelo[pck]))
     

            mensaje = file.read(MSJ_SIZE)

   

"""
El cliente solo va a necesitar un solo timer del paquete en vuelo mas antiguo, cuando se agota el tiempo de espera el cliente
retransmite el paquete N y todos los sucesivos a el. 

Cada vez que recibe un paquete, va a enviar un ACK de los paquetes recibidos correctamente hasta el momento que tiene 
el numero de secuencia mas alto.

"""