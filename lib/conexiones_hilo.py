from fileinput import filename
import os
import threading
import gestorPaquetes
import receiver
from socket import *
import sender_stop_wait_server
import sender_gobackn_server
import receiver_server


DATA = 0 #a veces llamado NOT_ACK
ACK = 1
UPLOAD = 2
DOWNLOAD = 3
REFUSED = 4
FIN = 5
ACK_CORRECT = 1
ACK_INCORRECT = 0

MAX_WAIT_HANDSHAKE = 30
MAX_TAMANIO_PERMITIDO = 6000000 #en bytes
MAX_WAIT_SERVIDOR = 50 #PELIGRO! TIMEOUT DEL SERVER!!
CARACTER_SEPARADOR = "-"

class Conexion(threading.Thread):
    def __init__(self,numero_hilo, conexion_cliente,protocolo,filePath,logger):
        threading.Thread.__init__(self)
        self.nombre = numero_hilo
        self.conexion_cliente = conexion_cliente
        self.ip_cliente = conexion_cliente[0]
        self.puerto_cliente = conexion_cliente[1] 
        self.skt = socket(AF_INET,SOCK_DGRAM)
        self.queue = []
        self.hay_data = False
        self.conexion_activa = True
        self.gestor_paquete = gestorPaquetes.Gestor_Paquete()
        self.protocolo = protocolo
        self.ruta_archivo = filePath
        self.logger = logger

    def pasar_data(self, paquete= b""):
        self.queue.append(paquete)
        self.hay_data = True

    def run(self):
        while True:
            if self.hay_data:
                break
        tiraBytes = self.queue.pop(0)
        if len(self.queue) == 0:
            self.hay_data = False
        paqueteBytes = self.gestor_paquete.pasarBytesAPaquete(tiraBytes)
        self.procesarHandshake(paqueteBytes)



    def enviar_archivo(self,file_name,filepath):
        self.logger.info(f"File name del archivo a enviar es: {file_name}")
        self.logger.info(f"EL file path del archivo a enviar es: {filepath}")
        if(self.protocolo == "GN"):
            self.logger.info("Se envia via protocolo Go Back N")
            sender = sender_gobackn_server.GoBackN(self.ip_cliente,self.puerto_cliente,file_name,filepath, self.logger)
        else:
            self.logger.info("Se envia via protocolo StopAndWait")
            sender = sender_stop_wait_server.StopWait(self.ip_cliente,self.puerto_cliente,file_name,filepath,self.logger)
            
        sender.start()
        while True:
            if self.hay_data:
                paqueteBytes = self.queue.pop(0)
                sender.pasar_data(paqueteBytes)
                if len(self.queue) == 0:
                    self.hay_data = False
                if paqueteBytes is None:
                    return
            if(sender.Termino == True):
                self.logger.info("El envio se ha realizado con exito")
                sender.join()
                self.conexion_activa = False
                return



    def recibir_archivo(self,file_name,filepath):
        self.logger.info(f"File name es: {file_name}")
        self.logger.info(f"EL file path es: {filepath}")
    
        receiver = receiver_server.Receiver(self.ip_cliente,self.puerto_cliente,filepath,file_name,self.logger)
        receiver.start()
        while True:
            if self.hay_data:
                paqueteBytes = self.queue.pop(0)
                receiver.pasar_data(paqueteBytes)
            
                if len(self.queue) == 0:
                    self.hay_data = False
                if paqueteBytes is None:
                    return
            if(receiver.Termino == True):
                self.logger.info("Se ha terminado el envio")
                receiver.join()
                self.conexion_activa = False
                return
    
    def esta_activa(self):
        return self.conexion_activa

    def procesarHandshake(self, paquete):
        self.logger.info("Procesando el handshake...")
        handshakeApropiado = self.chequearHandshakeApropiado(paquete)
        if (not handshakeApropiado) :
            self.logger.error("✗ Se envió un paquete que no es handshake, me voy")
            paqueteRefused = self.gestor_paquete.crearPaqueteRefused()
            self.skt.sendto(self.gestor_paquete.pasarPaqueteABytes(paqueteRefused),(self.ip_cliente,self.puerto_cliente))
            return False
        
        tamanioApropiado = self.chequearTamanio(paquete)
        if (not tamanioApropiado) :
            self.logger.error("✗ El tamaño pasado no es apropiado, mando ack de refused y me voy")
            paqueteRefused = self.gestor_paquete.crearPaqueteRefused()
            self.skt.sendto(self.gestor_paquete.pasarPaqueteABytes(paqueteRefused),(self.ip_cliente,self.puerto_cliente))
            return False

        archivoExiste = self.chequearExistenciaArchivo(paquete)
        if (not archivoExiste and paquete.esDownload()) :
                self.logger.error("✗ El archivo pedido no existe")
                paqueteRefused = self.gestor_paquete.crearPaqueteRefused()
                self.skt.sendto(self.gestor_paquete.pasarPaqueteABytes(paqueteRefused),(self.ip_cliente,self.puerto_cliente))
                return False

        self.enviarACKHandshake(ACK_CORRECT)

        if self.esHandshakeUpload(paquete) :
                self.logger.debug("Handshake de tipo UPLOAD")
                filepath,filename = self.obtener_ruta_y_nombre(paquete)
                self.recibir_archivo(filename,filepath)
        else :
                self.logger.debug("Handshake de tipo DOWNLOAD")
                filepath,filename = self.obtener_ruta_y_nombre(paquete)
                self.enviar_archivo(filename,filepath)
                
                return True

    def chequearHandshakeApropiado(self, paquete):
        return (paquete.esDownload() or paquete.esUpload())


    def obtener_ruta_y_nombre(self,paquete):
        nombre_archivo , tam = self.obtenerNombreYTamanio(paquete)
        return (self.ruta_archivo,nombre_archivo)

    def obtener_ruta_archivo_upload(self,paquete,starterPath):
        nombre_archivo , tam = self.obtenerNombreYTamanio(paquete)
        filepath= starterPath + "/" + nombre_archivo
        return filepath

    def obtenerNombreYTamanio(self, paquete):
        mensaje = paquete.obtenerMensaje()
        if paquete.esUpload() :
            nombre, tamanio = str(mensaje, "ascii").split(CARACTER_SEPARADOR)
            return nombre, int(tamanio)
        return str(mensaje, "ascii"), 0

    def chequearTamanio(self, paquete) :
        self.logger.debug("Se checkea el tamaño del paquete...")
        if paquete.esDownload() :
            return True

        nombre, tamanio = self.obtenerNombreYTamanio(paquete)
        if (tamanio >= MAX_TAMANIO_PERMITIDO):
            return False
        self.logger.debug("Tamaño del archivo valido")
        return True

    def chequearExistenciaArchivo(self, paquete) :
        self.logger.debug("Se chequea la existencia de archivo...")
        nombre, tamanio = self.obtenerNombreYTamanio(paquete)
        i = 0
        
        listOfFiles = os.listdir(self.ruta_archivo ) 
        if nombre in listOfFiles :
            return True
        return False


    def esHandshakeUpload(self, paquete):
        return paquete.esUpload()

    def enviarACKHandshake(self, agregado):
        gP = gestorPaquetes.Gestor_Paquete()
        pck = gP.crearPaqueteACK(agregado)
        
        pckBytes = gP.pasarPaqueteABytes(pck)

        self.skt.sendto(pckBytes,(self.ip_cliente,self.puerto_cliente))    
    