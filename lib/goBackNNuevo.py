from socket import *
import time
import enviador
import paquete

MSJ_SIZE = 5
N = 4 #tamanio de la ventana

class GoBackNNuevo(enviador.Enviador):


    def enviarPaquete(self):

        def __init__(self):
            super(GoBackNNuevo,self).__init()
            self.older_seq_number = 1
            self.new_seq_number = 1
            self.paquetesEnVuelo = []

        def enviarPaquete(self,file,entidad):
            mensaje = file.read(MSJ_SIZE)
            while True:
                if(self.new_seq_number < self.older_seq_number + N):
                    pck = self.gestorPaquetes.crearPaquete(self.new_seq_number,mensaje)
                    self.paquetesEnVuelo.append(pck)
                    entidad.enviarPaquete(self.gestorPaquetes.pasarPaqueteABytes(pck))
                    if(self.older_seq_number == self.new_seq_number):
                        timeout_start = time.time()
                    self.new_seq_number += 1
                    continue

                pck_recibido = entidad.recibirPaquete() #salgo del continue y obtengo el ultimo paquete recibido
                verificar = self.gestorPaquetes.verificarACK(pck_recibido) #verifico si el ack es el que esperaba (el del ultimo)
                if(verificar == True): #si lo es, entonces significa que los anteriores los recibi bien
                    for pck in range(len(self.paquetesEnVuelo)):
                        if(pck <= pck_recibido.obtenerSeqNumber()):
                            self.paquetesEnVuelo.remove(self.paquetesEnVuelo[pck])
                    self.older_seq_number = pck_recibido.obtenerSeqNumber()+1
                    if(self.older_seq_number == self.new_seq_number):
                        timeout_start = 0
                    else:
                        timeout_start = time.time()
                if(timeout_start == 0):
                    timeout_start = time.time()
                    for pck in self.paquetesEnVuelo:
                        entidad.enviarPaquete(self.gestorPaquetes.pasarPaqueteABytes(pck))
                if(len(mensaje) < 0):
                    break
                
                    







        return

"""
El cliente solo va a necesitar un solo timer del paquete en vuelo mas antiguo, cuando se agota el tiempo de espera el cliente
retransmite el paquete N y todos los sucesivos a el. 

Cada vez que recibe un paquete, va a enviar un ACK de los paquetes recibidos correctamente hasta el momento que tiene 
el numero de secuencia mas alto.

"""