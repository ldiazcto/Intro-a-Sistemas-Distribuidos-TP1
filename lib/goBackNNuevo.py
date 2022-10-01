from socket import *
import time
import enviador
import paquete

MSJ_SIZE = 5
N = 2 #tamanio de la ventana

class GoBackNNuevo(enviador.Enviador):

    # GO BACK N TIENE ACK ACUMULATIVOS, SI SE PIERDE UN PAQUETE ME VA A DEVOLVER EL ACK DEL ANTERIOR YA QUE VA A DESCARTAR LOS PAQUETES SIGUIENTES AL QUE PERDIO

    def __init__(self):
        self.older_seq_number = 1
        self.new_seq_number = 0
        self.paquetesEnVuelo = []
        self.acksRecibidos = []
        super(GoBackNNuevo,self).__init__()

    def enviar(self,mensaje,entidad):
        return 1

    def enviarPaquete(self,file,entidad):
        mensaje = file.read(MSJ_SIZE)
        i=0
        while (len(mensaje) > 0):
            #si el numero de sequencia del siguiente paquete a enviar es menor al numero de seq del primer paquete que envie __
            if(self.new_seq_number < self.older_seq_number + N):
                pck = self.gestorPaquetes.crearPaquete(mensaje)
                self.paquetesEnVuelo.append(pck)
                entidad.enviarPaquete(self.gestorPaquetes.pasarPaqueteABytes(pck))
                self.new_seq_number = pck.obtenerSeqNumber()
                if(self.older_seq_number == self.new_seq_number): #entrás cuando corriste la ventana entera
                    timeout_start = time.time()
                pck_recibido = entidad.recibirPaqueteBackN(timeout_start) #salgo del continue y obtengo el ultimo paquete recibido
                #me llegó ack, lo revisamos
                print("pck_recibido: ",pck_recibido)
                ackRecibido = self.gestorPaquetes.actualizarACK(pck_recibido)
                if(ackRecibido):
                    self.acksRecibidos.append(ackRecibido)
            #Quiero el ultimo ack nomas, si es True es porque los anteriores hasta ese llegaron bien
            print("ultimo pck recibido: ",pck_recibido)
            if (ackRecibido) : #SI RECIBO UN ACK, SIGNIFICA QUE RECIBI EL ACK DEL ULTIMO PAQUETE QUE LLEGO BIEN
                                # (ES DECIR QUE, TODOS LOS PAQUETES ANTERIORES TMB LLEGARON BIEN)
                #muevo el older_seq_number a la posicion siguiente al new_seq_number
                self.older_seq_number = pck_recibido.obtenerSeqNumber()+1 
                if(self.older_seq_number == pck_recibido.obtenerSeqNumber()): 
                    timeout_start = 0 #reinicio el timer porque los paquetes me llegaron bien, corro el older porque tengo que mandar paquetes nuevos 
                for pck in range(len(self.paquetesEnVuelo)): #borro los paquetes anteriores al ack que recibi, porque llegaron bien
                    if(pck <= pck_recibido.obtenerSeqNumber()):
                        self.paquetesEnVuelo.remove(self.paquetesEnVuelo[pck])
            if(timeout_start == 0): #SI SALTA TIMEOUT SIGNIFICA QUE PERDI UN PAQUETE Y POR ENDE TENGO QUE VOLVER A INICIAR EL TIMER Y
                                    # ENVIAR LOS PAQUETES QUE ME QUEDARON EN LA LISTA DE PAQUETES EN VUELO
                timeout_start = time.time()
                for pck in range(len(self.paquetesEnVuelo)):
                    if(pck > len(self.acksRecibidos)):
                        entidad.enviarPaquete(self.gestorPaquetes.pasarPaqueteABytes(self.paquetesEnVuelo[pck]))

            mensaje = file.read(MSJ_SIZE)
            """if(len(mensaje) > 0):
                print("older ",self.older_seq_number)
                print("iteracion: ",i)
                i += 1
                continue"""

        print("\n sali del while \n ")
        
            #falta código

        return 1

"""
El cliente solo va a necesitar un solo timer del paquete en vuelo mas antiguo, cuando se agota el tiempo de espera el cliente
retransmite el paquete N y todos los sucesivos a el. 

Cada vez que recibe un paquete, va a enviar un ACK de los paquetes recibidos correctamente hasta el momento que tiene 
el numero de secuencia mas alto.

"""