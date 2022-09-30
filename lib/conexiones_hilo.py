import os
import threading
import time
import gestorPaquetes
import receiver
from socket import *
import paquete

DATA = 0 #a veces llamado NOT_ACK
ACK = 1
UPLOAD = 2
DOWNLOAD = 3
REFUSED = 4
FIN = 5
ACK_CORRECT = 1

DIRECTORIO_BUSQUEDA = "/Users/abrildiazmiguez/Desktop/BDD_Servidor"
MAX_WAIT_HANDSHAKE = 30
MAX_TAMANIO_PERMITIDO = 30 #en bytes

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
        paquete = self.gestor_paquete.pasarBytesAPaquete(paqueteBytes)
        print("\npaquete es ", paquete)

        handshakeExitoso = self.procesarHandshake(paquete)
        if (not handshakeExitoso) :
            print("El handshake no funcó, me tengo que ir")
            return
        print("--Server: EL HANDSHAKE FUNCÓ!--")
        
        """
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
        if (self.gestor_paquete.verificar_mensaje_recibido(paquete) == True):
            paquete_ack = self.gestor_paquete.crearPaqueteACK(1)
            self.skt.sendto(self.gestor_paquete.pasarPaqueteABytes(paquete_ack),(self.ip_cliente,self.puerto_cliente))
        else:
            paquete_ack = self.gestor_paquete.crearPaqueteACK(0)
            self.skt.sendto(self.gestor_paquete.pasarPaqueteABytes(paquete_ack),(self.ip_cliente,self.puerto_cliente))
            #PONER AL QUE ESCRIBE EL ARCHIVO
        
    
    #POSIBLE BORRADO
    """def enviar_mensaje(self):
        self.skt.sendto("Respuesta".encode(),(self.ip_cliente,self.puerto_cliente))
    """

    def esta_activa(self):
        return self.conexion_activa

    def procesarHandshake(self, paquete):
        handshakeApropiado = self.chequearHandshakeApropiado(paquete)
        if (not handshakeApropiado) :
            print("Se envió un paquete que no es handshake, me voy")
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
                return False

        self.enviarACKHandshake(ACK_CORRECT)

        if self.esHandshakeUpload(paquete) :
                x=1
                print("Es de tipo upload")
                #lógica para el upload
        else :
                x=2
                print("Es de tipo download")
                #lógica para el download

        return True

    def chequearHandshakeApropiado(self, paquete):
        return (paquete.esDownload() or paquete.esUpload())



    def obtenerNombreYTamanio(self, mensaje):
        nombre, tamanio = str(mensaje, "ascii").split("-")
        return nombre, int(tamanio)

    def chequearTamanio(self, paquete) :
        if paquete.esDownload() :
            return True
        
        nombre, tamanio = self.obtenerNombreYTamanio(paquete.obtenerMensaje())
        if (tamanio >= MAX_TAMANIO_PERMITIDO):
            return False
        return True

    def chequearExistenciaArchivo(self, paquete) :
        nombre, tamanio = self.obtenerNombreYTamanio(paquete.obtenerMensaje())
        filenames = os.walk(DIRECTORIO_BUSQUEDA)
        print("recibido de os.walk = ", filenames)
        if nombre in filenames:
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
     