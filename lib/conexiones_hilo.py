import os
import threading
import time
import gestorPaquetes
import receiver
from socket import *
import paquete
import stopAndWait
import goBackN
from pathlib import Path
import sender_stop_wait_server
import sender_gobackn_server


DATA = 0 #a veces llamado NOT_ACK
ACK = 1
UPLOAD = 2
DOWNLOAD = 3
REFUSED = 4
FIN = 5
ACK_CORRECT = 1
ACK_INCORRECT = 0

MAX_WAIT_HANDSHAKE = 30
MAX_TAMANIO_PERMITIDO = 5000000 #en bytes
MAX_WAIT_SERVIDOR = 50 #PELIGRO! TIMEOUT DEL SERVER!!

class Conexion(threading.Thread):
    def __init__(self,numero_hilo, conexion_cliente):
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
        #self.ruta_archivo = ""

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



    def imprimir_mensaje(self, paqueteBytes):
        print ("Numero_hilo: ",self.nombre,"conexion:",self.conexion_cliente)
        print ("paqueteBytes: ",paqueteBytes)
        print("\n")

    def procesar_mensaje(self,paqueteBytes,file):
        paquete = self.gestor_paquete.pasarBytesAPaquete(paqueteBytes)

        print("El paqueteBytes recibido en procesar_mensaje es = ", paqueteBytes)
        print("El mensaje es recibido en procesar_mensaje es = ", paquete.obtenerMensaje())

        if (self.gestor_paquete.verificarPaqueteOrdenado(paquete) == True):
            if(paquete.esFin()):
                
                print("ES PAQUETE FIN: ")
                paquete_ack = self.gestor_paquete.crearPaqueteACK(ACK_CORRECT)
                print("El paquete ACK que voy a mandar por haber entrado a True es: ", self.gestor_paquete.pasarPaqueteABytes(paquete_ack))
                #time.sleep(10)
                self.skt.sendto(self.gestor_paquete.pasarPaqueteABytes(paquete_ack),(self.ip_cliente,self.puerto_cliente))
                print("Envié el paquete ACK positivo a esta ip y puerto ", (self.ip_cliente,self.puerto_cliente))
                file.close()
                self.conexion_activa = False
                return

            print("Al verificar el paquete, resulta que es True")
            paquete_ack = self.gestor_paquete.crearPaqueteACK(ACK_CORRECT)
            file.write(paquete.obtenerMensaje())
            print("El paquete ACK que voy a mandar por haber entrado a True es: ", self.gestor_paquete.pasarPaqueteABytes(paquete_ack))
            #time.sleep(10)
            self.skt.sendto(self.gestor_paquete.pasarPaqueteABytes(paquete_ack),(self.ip_cliente,self.puerto_cliente))
            print("Envié el paquete ACK positivo a esta ip y puerto ", (self.ip_cliente,self.puerto_cliente))
        else:
            print("Al verificar el paquete, resulta que es False")
            paquete_ack = self.gestor_paquete.crearPaqueteACK(ACK_INCORRECT)
            print(self.gestor_paquete.pasarPaqueteABytes(paquete_ack))
            #time.sleep(2)
            self.skt.sendto(self.gestor_paquete.pasarPaqueteABytes(paquete_ack),(self.ip_cliente,self.puerto_cliente))
        
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
                filepath = self.obtener_ruta_archivo_upload(paquete)
                file = open(filepath, 'wb')
                self.recibir_archivo(file)
                #lógica para el uploadobtenerNombreYTipo
        else :
                print("Es de tipo download")
                file_name = self.obtenerNombreYTamanio(paquete)
                self.enviar_archivo(file_name[0])
                """
                filepath, tipo = self.obtener_ruta_archivo_download(paquete)
                if(tipo == "stopAndWait"):
                    env = stopAndWait.StopAndWait()
                    env.enviarPaquete(filepath)
                else:
                    env = goBackN.GoBackN()
                    env.enviarPaquete(filepath)
                """
                #lógica para el download        
                #cargaPaquete = paquete.obtenerMensaje
                #Aca llamo a las funciones del cliente para manejo de paquetes y le paso el paquete OJO QUE HAY QUE GUARDAR LA RUTA EN LA CONEXION"""
    
                return True

    def chequearHandshakeApropiado(self, paquete):
        print("entre a procesar handshake apropiado")
        return (paquete.esDownload() or paquete.esUpload())


  
    """
    def obtener_ruta_archivo_download(self,paquete):
        nombre_archivo, tipo_envio = self.obtenerNombreYTipo(paquete)
        path = os.getcwd()
        new_path = path + "/lib"
        #print("Path de archivos",new_path)
        filepath= new_path + "/" + nombre_archivo
        return filepath

    def obtenerNombreYTipo(self, paquete):
        mensaje = paquete.obtenerMensaje()
        if paquete.esDownload() :
            nombre, tipo = str(mensaje, "ascii").split("-")
            return nombre, tipo
        return str(mensaje, "ascii"), 0
    """

    def obtener_ruta_archivo_upload(self,paquete):
        nombre_archivo , tam = self.obtenerNombreYTamanio(paquete)
        path = os.getcwd()
        new_path = path + "/lib"
        #print("Path de archivos",new_path)
        filepath= new_path + "/" + nombre_archivo
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
        
        path = os.getcwd()
        new_path = path + "/lib"
        print("Path de archivos",new_path)
        listOfFiles = os.listdir(new_path) 
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
    

    def recibir_archivo(self,file):
        time_start = time.time()
        while time.time() - time_start <=   MAX_WAIT_SERVIDOR:
            #print(time.time() - time_start)
            if self.conexion_activa == False:
                return
            if self.hay_data: #verifico si me pasaron nueva data
                time_start = time.time()
                paqueteBytes = self.queue.pop(0) #obtengo la data
                #print("\n\n-- En recibi_archivo, el paqueteBytes recien recibido es: ", paqueteBytes)
                if len(self.queue) == 0:
                    self.hay_data = False #si la cola queda vacia establezco que no hay mas data, por ahora
                if paqueteBytes is None:   # If you send `None`, the thread will exit.
                    return
                self.imprimir_mensaje(paqueteBytes)
                self.procesar_mensaje(paqueteBytes,file)
                #print("Volvi de procesar_mensaje, el paqueteBytes era: ", paqueteBytes)
                #print("\n\n")
        print("ESPERE SUFICIENTE NO ME MANDASTE NADA")
        self.conexion_activa = False
    
    def enviar_archivo(self,file_name):
        print("File name es:", file_name)
        sender = sender_gobackn_server.GoBackN(self.ip_cliente,self.puerto_cliente,file_name)
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