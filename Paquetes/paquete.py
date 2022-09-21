from asyncio.windows_events import NULL
import time
from Cliente import cliente
from time import time as timer

CHUNCKSIZE = 35
MAX_WAIT = 0.005
MAX_TRIES = 3

class Paquete:
    sequenceNumber = 0
    ackNumber = 0
    cliente = NULL
    
    def __init__(self,sequenceNumber,ackNumber):
        self.sequenceNumber = sequenceNumber
        self.ackNumber = ackNumber
        self.cliente = cliente()

    def esACK(self):
        if (self.sequenceNumber == 0):
            return True
        return False

    def leerArchivo(ruta):
        file = open(ruta,"r")
        if (file.is_file() == False):
            print("El archivo no existe")
            return #o qué devolvemos?
        return file

    #STOP AND WAIT
    def stopAndWait(self,file):
        if (file == NULL):
            return

        for chunck in iter(lambda: file.read(CHUNCKSIZE),b''): #leo de a 1 paquete #TE LEE TODO EL ARCHIVO
            i = 0
            salir = False
            timeout_start = time.time()
            timeout = MAX_WAIT
        
            #por hipótesis estamos dispuestos a enviar 3 veces el mismo paquete. Si ninguna de las tres es exitosa, hay un error en la conexión
            while ((i < MAX_TRIES) and (salir == False)) :
                llego = False
                self.cliente.mandarPaquete(self.cliente, chunck)
                while time.time() < timeout_start + timeout and llego == False:
                    llego = self.cliente.chequearSiLlegoACK()
                if (llego == True) :
                    salir = True
                i += 1  
                
            if (salir == False) :
                #nunca recibi el ack, error!
                return 0

        return 1 #despues revisamos qué devolver en cada caso de la función

    
    
    
#GO BACK N
#def goBackN():