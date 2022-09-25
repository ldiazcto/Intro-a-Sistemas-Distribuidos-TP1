#from asyncio.windows_events import NULL
from socket import *
import time
import enviador

MSJ_SIZE = 5
MAX_WAIT = 0.01
MAX_TRIES = 3
MAX_VENTANA = 10

class GoBackN(enviador.Enviador):

    def __init__(self):
        self.ackEsperado = 0
        self.paquetesEnVuelo = []
        self.timers = []

#Go back N
    def enviarPaquete(self, file, cliente):
        
        for mensaje in iter(lambda: file.read(MSJ_SIZE),b''):
            print(mensaje)
            
            if (len(self.paquetesEnVuelo) < MAX_VENTANA):
                print("Estoy por enviar el pck " + str(len(self.paquetesEnVuelo)))
                cliente.mandarPaquete(mensaje)
                self.paquetesEnVuelo.append(mensaje)
                self.timers.append(time.time()) #Ordenado de mas viejo a mas nuevo
            
            print("timer cero: ",self.timers[0])
            print("timer tope: ",self.timers[0] + MAX_WAIT)
            #esACK, ackRecibido = self.cliente.chequearSiLlegoACK()
            #if (ackRecibido == self.ackEsperado):
            #    print("Acá no debería entrar")
            #    self.timers.pop(0) #Esto elimina el timer mas viejo
            #    self.paquetesEnVuelo = self.paquetesEnVuelo.filter(lambda pck: pck.sequenceNumber != self.ackEsperado)
            #    self.ackEsperado+=1
            
        
            #Si el timer sono o si el ack recibido no es el esperado, se envian todos los paquetes que estan en paquetesEnVuelo
            #if ((time.time() >= self.timers[0] + MAX_WAIT) or (ackRecibido != self.ackEsperado)):
            if ((time.time() >= self.timers[0] + MAX_WAIT) ):
                print("saltó el timer")
                #self.timers = []
                #for msj in range(len(self.paquetesEnVuelo)):
                #    #cliente.mandarPaquete(pck.mensaje)
                #    print("Leo el msj " + self.paquetesEnVuelo[msj] + " numero " + msj)
                #    cliente.mandarPaquete(msj)
                #    self.timers.append(time.time())
            else:
                print("No saltó el timer aun")
                print("timer cero: ",self.timers[0])
                print("timer tope: ",self.timers[0] + MAX_WAIT)


        return 1

        
