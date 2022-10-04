from asyncio import SendfileNotAvailableError
from socket import *
import time
import gestorPaquetes
import threading
import sender_server




class StopWait(threading.Thread,sender_server.Sender_Server):

    def __init__(self,receiver_ip,receiver_port,filename,filePath,logger):
        threading.Thread.__init__(self)
        self.sender_socekt = socket(AF_INET,SOCK_DGRAM)
        self.sender_socekt.setblocking(False)
        self.receiver_ip = receiver_ip
        self.receiver_port = receiver_port
        self.gestorPaquetes = gestorPaquetes.Gestor_Paquete()
        self.cola = []
        self.filename = filename
        self.hay_data = False
        self.Termino = False
        self.filePath = filePath
        self.MAX_TRIES = 3
        self.MAX_WAIT = 3
        self.MSJ_SIZE = 2000
        self.logger = logger


    def run(self):
        self.enviar_archivo(self.logger)

    def enviar(self,mensaje):
        pck = self.gestorPaquetes.crearPaquete(mensaje)
        pckBytes = self.gestorPaquetes.pasarPaqueteABytes(pck)
        try:
            self.sender_socekt.sendto(pckBytes ,(self.receiver_ip,self.receiver_port))
        except SendfileNotAvailableError:
            print("-- El archivo no esta disponible --")
        cantidad_intentos = 1
        # self.logger.debug(f"\n-La cantidad intentos es {cantidad_intentos}")
        paqueteRecibido = self.recibirPaquete()

        while(paqueteRecibido == None and cantidad_intentos <= self.MAX_TRIES):
            try:
                self.sender_socekt.sendto(pckBytes ,(self.receiver_ip,self.receiver_port))
            except SendfileNotAvailableError:
                print("-- El archivo no esta disponible --")
            paqueteRecibido = self.recibirPaquete()
            cantidad_intentos += 1
            if(paqueteRecibido != None): 
                return (True,paqueteRecibido)

        if(cantidad_intentos > self.MAX_TRIES):
            self.Termino = True
            return (False,None)
            
        return (True,paqueteRecibido)

    def terminar_ejecucion(self, nuevo_estado):
        self.Termino = nuevo_estado

    def recibir_y_esperar(self, pckBytes):
        cantidad_intentos = 1
        paqueteRecibido = self.recibirPaquete()
        
        while(paqueteRecibido == None and cantidad_intentos <= self.MAX_TRIES):
            try:
                self.sender_socekt.sendto(pckBytes,(self.receiver_ip,self.receiver_port))
            except SendfileNotAvailableError:
                print("-- El archivo no esta disponible --")
            paqueteRecibido = self.recibirPaquete()
            if(paqueteRecibido != None): 
                break
            cantidad_intentos += 1
        
        return paqueteRecibido, cantidad_intentos

    def enviarPaquetes(self, file):

        mensaje = file.read(self.MSJ_SIZE)
        while(len(mensaje) > 0):
            intentar_mandar,paquete_recibido = self.enviar(mensaje)
            
            if (intentar_mandar == False):
                self.Termino =  True
                return
            verificar_ack = self.gestorPaquetes.actualizarACK(paquete_recibido) 
            intentar_mandar_ack = True
            if(verificar_ack == False): #EXTREMA SEGURIDAD --> ACK CORRUPTO
                cant_max_envios = 0
                while (cant_max_envios <= self.MAX_TRIES):
                    intentar_mandar_ack,paquete_recibido = self.enviar(mensaje)
                    cant_max_envios += 1
            if (intentar_mandar_ack == False):
                self.Termino =  True
                return
            mensaje = file.read(self.MSJ_SIZE)
        conexion_cerrada,pck_recibido = self.enviar_fin()
        if(conexion_cerrada == True):
            self.logger.info("Se ha cerrado la conexion con el protocolo StopAndWait con exito")
            self.Termino = True
        return
    
