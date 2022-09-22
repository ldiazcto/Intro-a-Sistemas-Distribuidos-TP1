from asyncio.windows_events import NULL
from socket import *
import time
from Enviador.enviador import Enviador

CHUNCKSIZE = 35
MAX_WAIT = 0.005
MAX_TRIES = 3

class StopAndWait(Enviador):

#STOP AND WAIT
    def enviarPaquete(self,file):
        if (file == NULL):
            
            return

        for chunck in iter(lambda: file.read(CHUNCKSIZE),b''): #leo de a 1 paquete #TE LEE TODO EL ARCHIVO
            i = 0
            salir = False
            timeout_start = time.time()
        
            #por hipótesis estamos dispuestos a enviar 3 veces el mismo paquete. Si ninguna de las tres es exitosa, hay un error en la conexión
            while ((i < MAX_TRIES) and (salir == False)) :
                llego = False
                self.cliente.mandarPaquete(self.cliente, chunck)
                while time.time() < timeout_start + MAX_WAIT and llego == False:
                    llego, ack = self.cliente.chequearSiLlegoACK()
                if (llego == True) :
                    salir = True
                i += 1
                
            if (salir == False) :
                #nunca recibi el ack, error!
                return 0

        return 1 #despues revisamos qué devolver en cada caso de la función
