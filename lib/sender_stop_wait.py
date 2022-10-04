from asyncio import SendfileNotAvailableError
from socket import *
import gestorPaquetes
import sender




BLOCKING = 1


class StopWait(sender.Sender):
    
    def __init__(self,server_ip,server_port,filename,filepath,logger):
        self.sender_socekt = socket(AF_INET,SOCK_DGRAM)
        self.sender_socekt.setblocking(False)
        self.receiver_ip = server_ip
        self.receiver_port = server_port
        self.filePath = filepath
        self.fileName = filename
        self.gestorPaquetes = gestorPaquetes.Gestor_Paquete()
        self.logger = logger
        self.MSJ_SIZE = 2000
        self.MAX_TRIES = 2
        self.MAX_WAIT = 10
        self.MAX_WAIT_GOBACKN = 5
        self.TAM_VENTANA = 150
        self.UPLOAD = 2
        self.CARACTER_SEPARADOR = "-"
        self.logger = logger


    def enviar(self,mensaje):
        pck = self.gestorPaquetes.crearPaquete(mensaje)
        pckBytes = self.gestorPaquetes.pasarPaqueteABytes(pck)
        self.sender_socekt.sendto(pckBytes ,(self.receiver_ip,self.receiver_port))
        cantidad_intentos = 1
        paqueteRecibido = self.recibirPaquete()
        while(paqueteRecibido == None and cantidad_intentos <= 3):
            try:
                self.sender_socekt.sendto(pckBytes ,(self.receiver_ip,self.receiver_port))
            except SendfileNotAvailableError:
                print("-- El archivo no esta disponible --")
            paqueteRecibido = self.recibirPaquete()
            cantidad_intentos += 1
            if(paqueteRecibido != None):
                return (True,paqueteRecibido)
        if(cantidad_intentos > 3):
            return (False,None)
        return (True,paqueteRecibido)
    

    def enviarPaquetes(self, file):
        mensaje = file.read(self.MSJ_SIZE)    
        while(len(mensaje) > 0):
            intentar_mandar,paquete_recibido = self.enviar(mensaje)
            if (intentar_mandar == False):
                return
            verificar_ack = self.gestorPaquetes.actualizarACK(paquete_recibido) 
            intentar_mandar_ack = True
            if(verificar_ack == False): #EXTREMA SEGURIDAD --> ACK CORRUPTO
                cant_max_envios = 0
                while (cant_max_envios <= 3):
                    intentar_mandar_ack,paquete_recibido = self.enviar(mensaje)
                    cant_max_envios += 1
            if (intentar_mandar_ack == False):
                return
            mensaje = file.read(self.MSJ_SIZE)
        conexion_cerrada, pck_recibido = self.enviar_fin()
        if(conexion_cerrada == True):
            self.logger.info("✓ Se ha cerrado la conexion con el protocolo StopAndWait con exito")
        return    