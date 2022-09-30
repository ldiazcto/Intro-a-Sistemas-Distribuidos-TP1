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
                mensaje = self.queue.pop(0) #obtengo la data
                if len(self.queue) == 0:
                    self.hay_data = False #si la cola queda vacia establezco que no hay mas data, por ahora
                if mensaje is None:   # If you send `None`, the thread will exit.
                    return
                self.imprimir_mensaje(mensaje)
                self.procesar_mensaje(mensaje)
                print("HASTA ACA LLEGO!")
                #self.enviar_mensaje()


    def imprimir_mensaje(self, message):
        print ("Numero_hilo:",self.nombre,"conexion:",self.conexion_cliente)
        print ("Mensaje:",message)
        print("\n")

    def procesar_mensaje(self,mensaje):
        if mensaje == "FIN":
            print ("CIERRO CONEXION")
            self.conexion_activa = False
        paquete = self.gestor_paquete.pasarBytesAPaquete(mensaje)

        self.recibirHandshake()

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


    def chequearHandshakeApropiado(paquete):
        return (paquete.esDownload() or paquete.esUpload())

    def obtenerTamanio(mensaje):
        nombre, tamanio = mensaje.split("-")
        return tamanio

    def chequearTamanio(self, paquete) :
        if paquete.esDownload() :
            return True
        
        tamanio = self.obtenerTamanio(paquete.obtenerMensaje())
        if (tamanio >= MAX_TAMANIO_PERMITIDO):
            return False
        return True

    def esHandshakeUpload(paquete):
        return paquete.esUpload()

    def enviarACKHandshake(self):
        #crear paquete
        gP = gestorPaquetes.Gestor_Paquete()
        pck = gP.crearPaqueteACK()
        
        #pasarlo a bytes
        pckBytes = gP.pasarPaqueteABytes(pck)

        #pasarlo con enviarPaquete 
        self.enviarPaquete(pckBytes)

    def recibirHandshake(self):
        time_start = time.time()
        paqueteRecibido = None
        while time.time() < time_start + MAX_WAIT_HANDSHAKE and paqueteRecibido == None:
                print("\nEntro al while")
                paqueteRecibido = self.recibirPaquete()
                print("Paquete es ", paqueteRecibido)
        
        if (paqueteRecibido == None) :
            print("Salto el timer, me voy")
        
        return paqueteRecibido
      