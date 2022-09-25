#from asyncio.windows_events import NULL
from socket import *
import time
import enviador

MSJ_SIZE = 5
MAX_WAIT = 0.005
MAX_TRIES = 3

class StopAndWait(enviador.Enviador):

    def __init__(self):
        enviador.Enviador.__init__(self)
        super().__init__()
    
#STOP AND WAIT
    def enviarPaquete(self,file, cliente):

        mensaje = file.read(MSJ_SIZE)
        while len(mensaje) > 0 :
            i = 0
            salir = False
        
            #por hipótesis estamos dispuestos a enviar 3 veces el mismo paquete. Si ninguna de las tres es exitosa, hay un error en la conexión
            while ((i < MAX_TRIES) and (salir == False)) :
                timeout_start = time.time()
                llego = False
                cliente.mandarPaquete(mensaje)
                while time.time() < timeout_start + MAX_WAIT and llego == False:
                    #llego, ack = self.cliente.chequearSiLlegoACK()
                #if (llego == True) :
                    #print("me llego ack, no se deberia imprimir esto")
                    #salir = True
                    x = 1
                i += 1
                print("Intento de envio numero", i)
                
            if (salir == False) :
                print("NUNCA ME LLEGO EL ACK, ME VOY -- bien que entramos aca")
                return 0
            
            mensaje = file.read(MSJ_SIZE)

        return 1 #despues revisamos qué devolver en cada caso de la función
