import os
import threading
import time
import gestorPaquetes
import receiver
from socket import *
import paquete
from pathlib import Path

DATA = 0 #a veces llamado NOT_ACK
ACK = 1
UPLOAD = 2
DOWNLOAD = 3
REFUSED = 4
FIN = 5
ACK_CORRECT = 1

DIRECTORIO_BUSQUEDA = "/Users/abrildiazmiguez/Desktop/BDD_Servidor"
MAX_WAIT_HANDSHAKE = 30
MAX_TAMANIO_PERMITIDO = 500 #en bytes
MAX_WAIT_SERVIDOR = 10 #30 segs

class Conexion(threading.Thread):
    def __init__(self,numero_hilo, conexion_cliente):
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
        #self.ruta_archivo = ""

    def pasar_data(self, paquete= b""):
        self.queue.append(paquete)
        self.hay_data = True

    def run(self):
        while True:
            if self.hay_data: #verifico si me pasaron nueva data
                break
        tiraBytes = self.queue.pop(0)
        if len(self.queue) == 0:
            self.hay_data = False
        paqueteBytes = self.gestor_paquete.pasarBytesAPaquete(tiraBytes)
        #self.procesarHandshake(paqueteBytes)
        time_start = time.time()
        while time.time() <= time_start + MAX_WAIT_SERVIDOR:
            if self.conexion_activa == False:
                return
            if self.hay_data: #verifico si me pasaron nueva data
                paqueteBytes = self.queue.pop(0) #obtengo la data
                if len(self.queue) == 0:
                    self.hay_data = False #si la cola queda vacia establezco que no hay mas data, por ahora
                if paqueteBytes is None:   # If you send `None`, the thread will exit.
                    return
                self.imprimir_mensaje(paqueteBytes)
                self.procesar_mensaje(paqueteBytes)
                #self.enviar_mensaje()


    def imprimir_mensaje(self, paqueteBytes):
        print ("Numero_hilo: ",self.nombre,"conexion:",self.conexion_cliente)
        print ("paqueteBytes: ",paqueteBytes)
        print("\n")

    def procesar_mensaje(self,paqueteBytes):
        if paqueteBytes == "FIN":
            print ("CIERRO CONEXION")
            self.conexion_activa = False
        
        #paquete = self.gestor_paquete.pasarBytesAPaquete(paqueteBytes)
        print("\npaquete es ", paqueteBytes)

        """
        print("Estoy por entrar a procesarHandshake")
        if (not self.handshakeRealizado) :
            handshakeExitoso = self.procesarHandshake(paquete)
            if (not handshakeExitoso) :
                print("El handshake no funcó, me tengo que ir")
                return
            self.handshakeRealizado = True
            print("--Server: EL HANDSHAKE FUNCÓ!--")
        
        
        #es el primero no hace falta verificar mensaje recibido
        if (paquete.esUpload()):
            cargaPaquete = paquete.obtenerMensaje
            nombreTamanio = cargaPaquete.split("-")
            if(tamanio > MAXTAMANIO):
                paqueteRefused = self.gestorPaquete.crearPaqueteRefused()
                self.skt.sendto(self.gestor_paquete.pasarPaqueteABytes(paqueteRefused),(self.ip_cliente,self.puerto_cliente))
            self.ruta_archivo = ruta+nombteTamanio[0]
            Receiver.abrirArchivo(self.ruta_archivo)
            paquete_ack = self.gestor_paquete.crearPaqueteACK(1)
            self.skt.sendto(self.gestor_paquete.pasarPaqueteABytes(paquete_ack),(self.ip_cliente,self.puerto_cliente))

        if (paquete.esDownload()):
            cargaPaquete = paquete.obtenerMensaje
            #Aca llamo a las funciones del cliente para manejo de paquetes y le paso el paquete OJO QUE HAY QUE GUARDAR LA RUTA EN LA CONEXION
""" 
        """
        if (paquete.esACK()): #no me gusta se podria hacer a traves del gesto
            paquete_ack = self.gestor_paquete.crearPaqueteACK(1)
            self.skt.sendto(self.gestor_paquete.pasarPaqueteABytes(paquete_ack),(self.ip_cliente,self.puerto_cliente))
            #Receiver.cerrarArchivo(self.ruta_archivo)
            self.conexion_activa = False
        """
        if (self.gestor_paquete.verificar_mensaje_recibido(paqueteBytes) == True):
            paquete_ack = self.gestor_paquete.crearPaqueteACK(1)
            print("mando ack verificado")
            self.skt.sendto(self.gestor_paquete.pasarPaqueteABytes(paquete_ack),(self.ip_cliente,self.puerto_cliente))
        else:
            paquete_ack = self.gestor_paquete.crearPaqueteACK(0)
            print("mando ack no verificado")
            self.skt.sendto(self.gestor_paquete.pasarPaqueteABytes(paquete_ack),(self.ip_cliente,self.puerto_cliente))
            #PONER AL QUE ESCRIBE EL ARCHIVO
        
    
    #POSIBLE BORRADO
    """def enviar_mensaje(self):
        self.skt.sendto("Respuesta".encode(),(self.ip_cliente,self.puerto_cliente))
    """

    def esta_activa(self):
        return self.conexion_activa

    def procesarHandshake(self, paquete):
        print("Entre a procesar Handshake")
        handshakeApropiado = self.chequearHandshakeApropiado(paquete)
        if (not handshakeApropiado) :
            print("Se envió un paquete que no es handshake, me voy")
            paqueteRefused = self.gestor_paquete.crearPaqueteRefused()
            self.skt.sendto(self.gestor_paquete.pasarPaqueteABytes(paqueteRefused),(self.ip_cliente,self.puerto_cliente))
            #CIERRO LA CONEXION ??
            return False
        
        tamanioApropiado = self.chequearTamanio(paquete)
        if (not tamanioApropiado) :
            print("El tamaño pasado no es apropiado, mando ack de refused y me voy")
            paqueteRefused = self.gestor_paquete.crearPaqueteRefused()
            self.skt.sendto(self.gestor_paquete.pasarPaqueteABytes(paqueteRefused),(self.ip_cliente,self.puerto_cliente))
            return False

        archivoExiste = self.chequearExistenciaArchivo(paquete)
        print("archivoExiste vale ", archivoExiste)
        if (not archivoExiste and paquete.esDownload()) :
                print("El archivo pedido no existe, me voy")
                #hay que establecer este protocolo
                paqueteRefused = self.gestor_paquete.crearPaqueteRefused()
                self.skt.sendto(self.gestor_paquete.pasarPaqueteABytes(paqueteRefused),(self.ip_cliente,self.puerto_cliente))
                return False

        self.enviarACKHandshake(ACK_CORRECT)

        if self.esHandshakeUpload(paquete) :
                print("Es de tipo upload")
                self.recibir_archivo()
                #lógica para el upload
        else :
                x=2
                print("Es de tipo download")
                #lógica para el download

        return True

    def chequearHandshakeApropiado(self, paquete):
        print("entre a procesar handshake apropiado")
        return (paquete.esDownload() or paquete.esUpload())



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
        #print(Path.cwd())
        #dirname = os.path.dirname(".")
  
        #Print the directory name  
        #print(dirname)
        #return True
        nombre, tamanio = self.obtenerNombreYTamanio(paquete)
        i = 0
        
        path = os.getcwd()
        new_path = path + "/lib"
        print("Path de archivos",new_path)
        listOfFiles = os.listdir(new_path)  
        #print(listOfFiles)
        #for filename in listOfFiles:
            #print("archivo: ", filename)
        """
        resultado = os.walk(".")
        listGrande = list(resultado)
        tupla = listGrande[0]
        names = tupla[2]
        print("Archivos son:", names)
        """
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
    

    def recibir_archivo(self):
        time_start = time.time()
        while time.time() <= time_start + MAX_WAIT_SERVIDOR:
            if self.conexion_activa == False:
                return
            if self.hay_data: #verifico si me pasaron nueva data
                paqueteBytes = self.queue.pop(0) #obtengo la data
                if len(self.queue) == 0:
                    self.hay_data = False #si la cola queda vacia establezco que no hay mas data, por ahora
                if paqueteBytes is None:   # If you send `None`, the thread will exit.
                    return
                self.imprimir_mensaje(paqueteBytes)
                self.procesar_mensaje(paqueteBytes)
            