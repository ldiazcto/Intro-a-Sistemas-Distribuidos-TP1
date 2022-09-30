from socket import *
import time
import enviador
import paquete

MSJ_SIZE = 5
N = 2 #tamanio de la ventana

class GoBackNNuevo(enviador.Enviador):


    def __init__(self):
        self.older_seq_number = 1
        self.new_seq_number = 0
        self.paquetesEnVuelo = []
        self.paquetesRecibidos = []
        super(GoBackNNuevo,self).__init__()

    def enviar(self,mensaje,entidad):
        return 1

    def enviarPaquete(self,file,entidad):
        mensaje = file.read(MSJ_SIZE)
        i=0
        while True:
            if(self.new_seq_number < self.older_seq_number + N):
                pck = self.gestorPaquetes.crearPaquete(mensaje)
                self.paquetesEnVuelo.append(pck)
                entidad.enviarPaquete(self.gestorPaquetes.pasarPaqueteABytes(pck))
                self.new_seq_number = pck.obtenerSeqNumber()
                if(self.older_seq_number == self.new_seq_number): #entrás cuando corriste la ventana entera
                    timeout_start = time.time()
                pck_recibido = entidad.recibirPaqueteBackN() #salgo del continue y obtengo el ultimo paquete recibido
                if (pck_recibido == None) :
                    #no me llegó ack, mando nuevo paquete si puedo
                    mensaje = file.read(MSJ_SIZE)
                    continue
                #me llegó ack, lo revisamos
                print("pck recibido es ", pck_recibido)
                ackEsperado = self.gestorPaquetes.actualizarACK(pck_recibido)
                if (ackEsperado) :
                    #es el ack que yo esperaba, puedo enviar otro paquete
                    self.older_seq_number = pck_recibido.obtenerSeqNumber()+1 
                    if(self.older_seq_number == pck_recibido.obtenerSeqNumber()):
                        timeout_start = 0 
                    for pck in range(len(self.paquetesEnVuelo)):
                        if(pck <= pck_recibido.obtenerSeqNumber()):
                            self.paquetesEnVuelo.remove(self.paquetesEnVuelo[pck])
                else :
                    #no me llegó el ack que quería
                    #necesito reenviar este paquete
                    timeout_start = time.time()
                    for pck in self.paquetesEnVuelo:
                        entidad.enviarPaquete(self.gestorPaquetes.pasarPaqueteABytes(pck))

                mensaje = file.read(MSJ_SIZE)
                if(len(mensaje) > 0):
                    print("older ",self.older_seq_number)
                    print("iteracion: ",i)
                    i += 1
                    continue

            print("\n sali del while \n ")
            break
        
            #falta código

        return 1

"""
El cliente solo va a necesitar un solo timer del paquete en vuelo mas antiguo, cuando se agota el tiempo de espera el cliente
retransmite el paquete N y todos los sucesivos a el. 

Cada vez que recibe un paquete, va a enviar un ACK de los paquetes recibidos correctamente hasta el momento que tiene 
el numero de secuencia mas alto.

"""