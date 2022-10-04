from asyncio import SendfileNotAvailableError
import os
from socket import *
import time
import gestorPaquetes
import threading
import sender_server

MSJ_SIZE = 2000
TAM_VENTANA = 150 #tamanio de la ventana
MAX_WAIT_GOBACKN = 5
MAX_WAIT_ACKS = 5
MAX_WAIT_FIN = 10
UPLOAD = 2

class GoBackN(threading.Thread,sender_server.Sender_Server):
    
    def __init__(self,receiver_ip,receiver_port,filename, filePath,logger):
        threading.Thread.__init__(self)
        self.sender_socekt = socket(AF_INET,SOCK_DGRAM)
        self.sender_socekt.setblocking(False)
        self.receiver_ip = receiver_ip
        self.receiver_port = receiver_port
        self.gestorPaquetes = gestorPaquetes.Gestor_Paquete()
        self.cola = []
        self.filename = filename
        self.hay_data = False
        self.older_seq_number = 1
        self.new_seq_number = 0
        self.paquetesEnVuelo = []
        self.Termino = False
        self.filePath = filePath
        self.MAX_TRIES = 3
        self.MAX_WAIT = 3
        self.MSJ_SIZE = 2000
        self.logger = logger
        self.conexion_activa = True


    def run(self):
        self.enviar_archivo(self.logger)


    def enviarPaquetes(self,file):
        mensaje = "entrar en ciclo"
        timeout_start = 0
        while (True):
            if(self.conexion_activa == False):
                return
            if(self.new_seq_number < self.older_seq_number + TAM_VENTANA):
                mensaje = file.read(self.MSJ_SIZE)
                if(len(mensaje) != 0):
                    pck = self.gestorPaquetes.crearPaquete(mensaje)
                    self.paquetesEnVuelo.append(pck)
                    try:
                        self.sender_socekt.sendto(self.gestorPaquetes.pasarPaqueteABytes(pck),(self.receiver_ip,self.receiver_port))
                    except SendfileNotAvailableError:
                        self.logger.error("✗ El archivo no esta disponible ")
                    self.new_seq_number = pck.obtenerSeqNumber()
                    if(self.older_seq_number == self.new_seq_number):
                        timeout_start = time.time()    
                    continue
                
            if(len(self.paquetesEnVuelo) == 0):
                break
            pckRecibido, esACKEsperado = self.recibirPaqueteACK()
            if (esACKEsperado) :
                cant_paquetes_a_popear =  pckRecibido.obtenerSeqNumber() - self.older_seq_number 
                self.older_seq_number = pckRecibido.obtenerSeqNumber()+1
                for i in range(cant_paquetes_a_popear + 1 ): 
                    pck = self.paquetesEnVuelo.pop(0)
                if(self.older_seq_number == self.new_seq_number):
                    break
                else:    
                    timeout_start = time.time() 
            var = time.time()
            saltoTimerReenvio = (var - timeout_start)  >= MAX_WAIT_GOBACKN
            if(saltoTimerReenvio and timeout_start != 0):
                self.logger.error("\n\n Timeout... \n\n")
                timeout_start = time.time()
                for pck in self.paquetesEnVuelo:
                    try:
                        self.sender_socekt.sendto(self.gestorPaquetes.pasarPaqueteABytes(pck),(self.receiver_ip,self.receiver_port))
                    except SendfileNotAvailableError:
                        self.logger.error("✗ El archivo no esta disponible ")
        conexion_cerrada,pck_recibido = self.enviar_fin()
        if(conexion_cerrada == True):
            self.logger.info("Se ha cerrado la conexion con el protocolo GoBackN con exito")
        self.Termino = True
        return

    def recibirPaqueteACK(self) :
        pckRecibido = self.recibirPaqueteBackN()
        ackRecibido = self.gestorPaquetes.actualizarACK(pckRecibido)
        return pckRecibido, ackRecibido
    

    def recibirPaqueteBackN(self):
        if (self.hay_data == False):
            return None
        paqueteString = self.cola.pop(0)
        if(len(self.cola) == 0):
            self.hay_data = False
        return self.gestorPaquetes.pasarBytesAPaquete(paqueteString)

    def terminar_ejecucion(self, nuevo_estado):
        return

    def recibir_y_esperar(self, pckBytes):
        cantidad_intentos = 1
        paqueteRecibido = self.recibirPaquete()
        while(paqueteRecibido == None and cantidad_intentos <= 3):

            paqueteRecibido = self.recibirPaquete()
            cantidad_intentos += 1
        return paqueteRecibido, cantidad_intentos
    



