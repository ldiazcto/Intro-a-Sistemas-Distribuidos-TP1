from socket import *
import time
import enviador
import paquete

MSJ_SIZE = 5
N = 2 #tamanio de la ventana
MAX_WAIT_GOBACKN = 0.9
MAX_TRIES = 3

class GoBackNNuevo(enviador.Enviador):

    # GO BACK N TIENE ACK ACUMULATIVOS, SI SE PIERDE UN PAQUETE ME VA A DEVOLVER EL ACK DEL ANTERIOR YA QUE VA A DESCARTAR LOS PAQUETES SIGUIENTES AL QUE PERDIO

    def __init__(self):
        self.older_seq_number = 0
        self.new_seq_number = 0
        self.paquetesEnVuelo = []
        super(GoBackNNuevo,self).__init__()

    def enviar(self,mensaje,entidad):
        return 1

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
            
            # -- RECIBIR ACK --
            pck_recibido = entidad.recibirPaqueteBackN() #obtengo el ultimo paquete recibido
            print("pck_recibido: ",pck_recibido)
            ackRecibido = self.gestorPaquetes.actualizarACK(pck_recibido)
            
            # -- VERIFICACION DE ACK --
            if (ackRecibido == True) : #SI RECIBO UN ACK, SIGNIFICA QUE RECIBI EL ACK DEL ULTIMO PAQUETE QUE LLEGO BIEN
                                        # (ES DECIR QUE, TODOS LOS PAQUETES ANTERIORES TMB LLEGARON BIEN)
                #muevo el older_seq_number a la posicion siguiente al new_seq_number
                self.older_seq_number = pck_recibido.obtenerSeqNumber()+1 
                timeout_start = time.time() #reinicio el timer porque los paquetes me llegaron bien, corro el older porque tengo que mandar paquetes nuevos 
                self.paquetesEnVuelo.pop(0) #borro los paquetes anteriores al ack que recibi, porque llegaron bien
                    

            # -- REENVIAR PCKS EN CASO DE ERROR --
            if(ackRecibido == False and timeout_start + MAX_WAIT_GOBACKN <= time.time() ): #SI SALTO TIMEOUT, ENTONCES PERDI UN PAQUETE Y POR ENDE TENGO 
                                    #QUE VOLVER A INICIAR EL TIMER Y ENVIAR LOS PAQUETES QUE ME QUEDARON EN LA LISTA DE PAQUETES EN VUELO
                timeout_start = time.time()
                for pck in range(len(self.paquetesEnVuelo)):
                    entidad.enviarPaquete(self.gestorPaquetes.pasarPaqueteABytes(self.paquetesEnVuelo[pck]))
     

            mensaje = file.read(MSJ_SIZE)

        # -- NO TENGO M'AS PARA LEER, SOLO RECIBO Y REENVIO --
        i = 0
        while time.time() <= timeout_start + MAX_WAIT_GOBACKN and i <= MAX_TRIES:
            # -- RECIBIR ACK --
            pck_recibido = entidad.recibirPaqueteBackN() #obtengo el ultimo paquete recibido
            print("pck_recibido: ", pck_recibido)
            ackRecibido = self.gestorPaquetes.actualizarACK(pck_recibido)
            
            # -- VERIFICACION DE ACK --
            if (ackRecibido == True) : #SI RECIBO UN ACK, SIGNIFICA QUE RECIBI EL ACK DEL ULTIMO PAQUETE QUE LLEGO BIEN
                                        # (ES DECIR QUE, TODOS LOS PAQUETES ANTERIORES TMB LLEGARON BIEN)
                #muevo el older_seq_number a la posicion siguiente al new_seq_number
                print(" -------Entre al primer if-------")
                self.older_seq_number = pck_recibido.obtenerSeqNumber()+1 
                timeout_start = time.time() #reinicio el timer porque los paquetes me llegaron bien, corro el older porque tengo que mandar paquetes nuevos 
                self.paquetesEnVuelo.pop(0) #borro los paquetes anteriores al ack que recibi, porque llegaron bien
                    
            else :
                i +=1
            # -- REENVIAR PCKS EN CASO DE ERROR --
            if(ackRecibido == False and timeout_start + MAX_WAIT_GOBACKN <= time.time() ): #SI SALTO TIMEOUT, ENTONCES PERDI UN PAQUETE Y POR ENDE TENGO 
                                    #QUE VOLVER A INICIAR EL TIMER Y ENVIAR LOS PAQUETES QUE ME QUEDARON EN LA LISTA DE PAQUETES EN VUELO
                print(" \nEntre al segundo if\n")
                timeout_start = time.time()
                for pck in range(len(self.paquetesEnVuelo)):
                    entidad.enviarPaquete(self.gestorPaquetes.pasarPaqueteABytes(self.paquetesEnVuelo[pck]))



        print("\n sali de los dos whiles, todo deber'ia haber sido procesado \n ")
    
        return 1

"""
El cliente solo va a necesitar un solo timer del paquete en vuelo mas antiguo, cuando se agota el tiempo de espera el cliente
retransmite el paquete N y todos los sucesivos a el. 

Cada vez que recibe un paquete, va a enviar un ACK de los paquetes recibidos correctamente hasta el momento que tiene 
el numero de secuencia mas alto.

"""