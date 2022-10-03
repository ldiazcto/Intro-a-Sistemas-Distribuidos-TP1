import time
from socket import *
import gestorPaquetes
import os
import select

DATA = 0 #a veces llamado NOT_ACK
ACK = 1
UPLOAD = 2
DOWNLOAD = 3
REFUSED = 4
FIN = 5
ACK_CORRECT = 1
ACK_INCORRECT = 0

MAX_TRIES = 3
MAX_WAIT_ACKS = 5
MAX_WAIT_FIN = 10
MAX_WAIT = 10

MAX_WAIT_HANDSHAKE = 30
MAX_TAMANIO_PERMITIDO = 5000000 #en bytes
MAX_WAIT_SERVIDOR = 50 #PELIGRO! TIMEOUT DEL SERVER!!

class Receiver():  
    
    def __init__(self,receiver_ip,receiver_port,sender_ip,sender_port,):
        self.receiver_socekt = socket(AF_INET,SOCK_DGRAM)
        self.receiver_socekt.bind((receiver_ip,receiver_port)) #''  es para que escuche a todos --- serverPort es por d'onde escucha el server
        self.receiver_socekt.setblocking(False)
        self.sender_ip = sender_ip
        self.sender_port = sender_port
        self.receiver_ip = receiver_ip
        self.receiver_port = receiver_port
        self.gestor_paquete = gestorPaquetes.Gestor_Paquete()
        self.older_seq_number = 1
        self.new_seq_number = 0
        self.paquetesEnVuelo = []


    def recibir_archivo(self,filename):
        path = os.getcwd()
        new_path = path + "/lib"
        #print("Path de archivos",new_path)
        filepath= new_path + "/" + "hola4.txt"
        file_stats = os.stat(filepath)
        file_size = file_stats.st_size
        handshake_establecido = self.entablarHandshake("hola2.txt")
        if(handshake_establecido):
            file = open(filepath,'wb')
            self.recibir_Paquetes(file)
            file.close()
        else:
            print("FALLO EL HANDSHAKE")
            return


    def recibir_Paquetes(self,file):

        time_start = time.time()
        while time.time() - time_start <=   MAX_WAIT_SERVIDOR:
            """
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
                """
            lista_sockets_listos = select.select([self.receiver_socekt], [], [], 0)
            if not lista_sockets_listos[0]:
                continue
            paqueteBytes, sourceAddress = self.receiver_socekt.recvfrom(2048)
            time_start = time.time()
                
            #self.imprimir_mensaje(paqueteBytes)
            self.procesar_mensaje(paqueteBytes,file)
            #print("Volvi de procesar_mensaje, el paqueteBytes era: ", paqueteBytes)
            #print("\n\n")
        print("ESPERE SUFICIENTE NO ME MANDASTE NADA")

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
                self.receiver_socekt.sendto(self.gestor_paquete.pasarPaqueteABytes(paquete_ack),(self.sender_ip,self.sender_port))
                print("Envié el paquete ACK positivo a esta ip y puerto ", (self.sender_ip,self.sender_port))
                file.close()
                self.conexion_activa = False
                return

            print("Al verificar el paquete, resulta que es True")
            paquete_ack = self.gestor_paquete.crearPaqueteACK(ACK_CORRECT)
            file.write(paquete.obtenerMensaje())
            print("El paquete ACK que voy a mandar por haber entrado a True es: ", self.gestor_paquete.pasarPaqueteABytes(paquete_ack))
            #time.sleep(10)
            self.receiver_socekt.sendto(self.gestor_paquete.pasarPaqueteABytes(paquete_ack),(self.sender_ip,self.sender_port))
            print("Envié el paquete ACK positivo a esta ip y puerto ", (self.sender_ip,self.sender_port))    
        else:
            print("Al verificar el paquete, resulta que es False")
            paquete_ack = self.gestor_paquete.crearPaqueteACK(ACK_INCORRECT)
            print(self.gestor_paquete.pasarPaqueteABytes(paquete_ack))
            #time.sleep(2)
            self.receiver_socekt.sendto(self.gestor_paquete.pasarPaqueteABytes(paquete_ack),(self.sender_ip,self.sender_port))
            print("Envié el paquete ACK Negativo a esta ip y puerto ", (self.sender_ip,self.sender_port))
                


    def crearPaqueteHandshake_download(self, fileName):
        return self.gestor_paquete.crearPaqueteHandshake(DOWNLOAD, fileName)



    def entablarHandshake(self, fileName):
        paquete = self.crearPaqueteHandshake_download(fileName)
        paqueteBytes = self.gestor_paquete.pasarPaqueteABytes(paquete)
        i = 0
        while i <= MAX_TRIES:
                self.receiver_socekt.sendto(paqueteBytes,(self.sender_ip,self.sender_port))
                paqueteRecibido = self.recibirPaquete()
                #TIMEOUTEA VUELVO A ENVIAR EL HANDSHAKE
                if (paqueteRecibido == None):
                        print(i)
                        i += 1
                        continue
                esPaqueteOrdenado = self.gestor_paquete.verificarACK(paqueteRecibido)
                if (esPaqueteOrdenado) :
                        return True
                esPaqueteRefused = self.gestor_paquete.verificarRefused(paqueteRecibido)
                if (esPaqueteRefused) :
                        return False
                i +=1

        return False

    
    def recibirPaquete(self):
        timeout_start = time.time()
        while True:
                lista_sockets_listos = select.select([self.receiver_socekt], [], [], 0)
                var = time.time()
                if ((var - timeout_start) >= (MAX_WAIT)):
                        return None
                if not lista_sockets_listos[0]:
                        continue
                paqueteString, sourceAddress = self.receiver_socekt.recvfrom(2048)
                print("recibirPaquete: el string del paquete es: ", paqueteString)
                return self.gestor_paquete.pasarBytesAPaquete(paqueteString)