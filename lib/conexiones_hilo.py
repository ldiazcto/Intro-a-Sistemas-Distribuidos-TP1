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

class Conexion(threading.Thread):
    def __init__(self,numero_hilo, conexion_cliente,protocolo,filePath,logger):
        threading.Thread.__init__(self)
        self.nombre = numero_hilo
        self.conexion_cliente = conexion_cliente
        self.ip_cliente = conexion_cliente[0]
        self.puerto_cliente = conexion_cliente[1] #por ac'a escribe o escucha el cliente? --> ambos 
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
            if self.hay_data: #verifico si me pasaron nueva data
                break
        #este pop y procesamiento inicial est'a bien, pero tiene que mandar esa tira inicial en el handshake, sino se pierde ese paquete
        tiraBytes = self.queue.pop(0)
        if len(self.queue) == 0:
            self.hay_data = False
        paqueteBytes = self.gestor_paquete.pasarBytesAPaquete(tiraBytes)
        self.procesarHandshake(paqueteBytes)



    def enviar_archivo(self,file_name,filepath):
        print("File name es:", file_name)
        print("EL file path es: ", filepath)
        if(self.protocolo == "GN"):
            print("Soy GOBACKN")
            sender = sender_gobackn_server.GoBackN(self.ip_cliente,self.puerto_cliente,file_name,filepath)
        else:
            print("SoY STOP AND WAIT")
            sender = sender_stop_wait_server.StopWait(self.ip_cliente,self.puerto_cliente,file_name,filepath)
            
        sender.start()
        while True:
            if self.hay_data: #verifico si me pasaron nueva data
                paqueteBytes = self.queue.pop(0) #obtengo la data
                sender.pasar_data(paqueteBytes)
                #print("\n\n-- En recibi_archivo, el paqueteBytes recien recibido es: ", paqueteBytes)
                if len(self.queue) == 0:
                    self.hay_data = False #si la cola queda vacia establezco que no hay mas data, por ahora
                if paqueteBytes is None:   # If you send `None`, the thread will exit.
                    return
            if(sender.Termino == True):
                self.logger.info("Se ha terminado el envio")
                sender.join()
                self.conexion_activa = False
                return




    def recibir_archivo(self,file_name,filepath):
        print("File name es:", file_name)
        print("EL file path es: ", filepath)
    
        receiver = receiver_server.Receiver(self.ip_cliente,self.puerto_cliente,filepath,file_name)
        receiver.start()
        while True:
            if self.hay_data: #verifico si me pasaron nueva data
                paqueteBytes = self.queue.pop(0) #obtengo la data
                receiver.pasar_data(paqueteBytes)
                #print("\n\n-- En recibi_archivo, el paqueteBytes recien recibido es: ", paqueteBytes)
                if len(self.queue) == 0:
                    self.hay_data = False #si la cola queda vacia establezco que no hay mas data, por ahora
                if paqueteBytes is None:   # If you send `None`, the thread will exit.
                    return
            if(receiver.Termino == True):
                self.logger.info("Se termino el envio")
                receiver.join()
                self.conexion_activa = False
                return
    



    def esta_activa(self):
        return self.conexion_activa


#-------------PROCESAR HANDSHAKE-----------

    def procesarHandshake(self, paquete):
        self.logger.info("Se entro a procesar Handshake")
        handshakeApropiado = self.chequearHandshakeApropiado(paquete)
        if (not handshakeApropiado) :
            print("Se envió un paquete que no es handshake, me voy")
            paqueteRefused = self.gestor_paquete.crearPaqueteRefused()
            self.skt.sendto(self.gestor_paquete.pasarPaqueteABytes(paqueteRefused),(self.ip_cliente,self.puerto_cliente))
            #CIERRO LA CONEXION ??
            return False
        
        tamanioApropiado = self.chequearTamanio(paquete)
        if (not tamanioApropiado) :
            self.logger.debug("El tamaño pasado no es apropiado, mando ack de refused y me voy")
            paqueteRefused = self.gestor_paquete.crearPaqueteRefused()
            self.skt.sendto(self.gestor_paquete.pasarPaqueteABytes(paqueteRefused),(self.ip_cliente,self.puerto_cliente))
            return False

        archivoExiste = self.chequearExistenciaArchivo(paquete)
        print("archivoExiste vale ", archivoExiste)
        if (not archivoExiste and paquete.esDownload()) :
                self.logger.error("El archivo pedido no existe, me voy")
                #hay que establecer este protocolo
                paqueteRefused = self.gestor_paquete.crearPaqueteRefused()
                self.skt.sendto(self.gestor_paquete.pasarPaqueteABytes(paqueteRefused),(self.ip_cliente,self.puerto_cliente))
                return False

        self.enviarACKHandshake(ACK_CORRECT)

        if self.esHandshakeUpload(paquete) :
                print("Es de tipo upload")
                filepath,filename = self.obtener_ruta_y_nombre(paquete)
                self.recibir_archivo(filename,filepath)
        else :
                print("Es de tipo download")
                filepath,filename = self.obtener_ruta_y_nombre(paquete)
                self.enviar_archivo(filename,filepath)
                
                return True




#-------- FUNCIONES AUXILIARES HANDSHAKE-----------

    def chequearHandshakeApropiado(self, paquete):
        print("entre a procesar handshake apropiado")
        return (paquete.esDownload() or paquete.esUpload())


    def obtener_ruta_y_nombre(self,paquete):
        nombre_archivo , tam = self.obtenerNombreYTamanio(paquete)
        return (self.ruta_archivo,nombre_archivo)

    def obtener_ruta_archivo_upload(self,paquete,starterPath):
        nombre_archivo , tam = self.obtenerNombreYTamanio(paquete)
        #print("Path de archivos",new_path)
        filepath= starterPath + "/" + nombre_archivo
        return filepath

    def obtenerNombreYTamanio(self, paquete):
        mensaje = paquete.obtenerMensaje()
        if paquete.esUpload() :
            nombre, tamanio = str(mensaje, "ascii").split("-")
            return nombre, int(tamanio)
        return str(mensaje, "ascii"), 0

    def chequearTamanio(self, paquete) :
        print("entre a chequearTamanio")
        if paquete.esDownload() :
            return True
        MAX_TAMANIO_PERMITIDO
        nombre, tamanio = self.obtenerNombreYTamanio(paquete)
        if (tamanio >= MAX_TAMANIO_PERMITIDO):
            return False
        return True

    def chequearExistenciaArchivo(self, paquete) :
        print("Entre a chequear Existencia Archivo")
        nombre, tamanio = self.obtenerNombreYTamanio(paquete)
        i = 0
        
        print("Path de archivos", self.ruta_archivo )
        listOfFiles = os.listdir(self.ruta_archivo ) 
        if nombre in listOfFiles :
            return True
        return False



    def esHandshakeUpload(self, paquete):
        return paquete.esUpload()




    def enviarACKHandshake(self, agregado):
        #crear paquete
        gP = gestorPaquetes.Gestor_Paquete()
        pck = gP.crearPaqueteACK(agregado)
        
        #pasarlo a bytes
        pckBytes = gP.pasarPaqueteABytes(pck)

        self.skt.sendto(pckBytes,(self.ip_cliente,self.puerto_cliente))
    

    
    
    