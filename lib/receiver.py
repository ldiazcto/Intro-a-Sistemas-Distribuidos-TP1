import time
from socket import *
import gestorPaquetes
import os
import select


ACK = 1
DOWNLOAD = 3
REFUSED = 4
FIN = 5
ACK_CORRECT = 1
ACK_INCORRECT = 0

MAX_TRIES = 3
MAX_WAIT = 10

MAX_WAIT_SERVIDOR = 50 #PELIGRO! TIMEOUT DEL SERVER!!

class Receiver():  
    
    def __init__(self, sender_ip, sender_port, file_path, file_name, logger ):
        self.receiver_socekt = socket(AF_INET,SOCK_DGRAM)
        self.receiver_socekt.setblocking(False)
        self.sender_ip = sender_ip
        self.sender_port = sender_port
        self.gestor_paquete = gestorPaquetes.Gestor_Paquete()
        self.Termino = False
        self.file_path = file_path
        self.file_name = file_name
        self.logger = logger


    # Dados el path y el file name enviados al constructor, se entabla el handshake y se recibe el archivo
    # Se devuelve True en caso de éxito y False en caso de error
    def recibir_archivo(self):
        new_path = self.file_path + "/" + self.file_name
        filepath= new_path
        handshake_establecido = self.entablarHandshake(self.file_name)
        if(handshake_establecido):
            file = open(filepath,'wb')
            print("ABRI EL ARCHIVO")
            self.recibir_Paquetes(file)
            file.close()
            return True
        else:
            print("FALLO EL HANDSHAKE")
            return False


    def recibir_Paquetes(self,file):

        time_start = time.time()
        while time.time() - time_start <=   MAX_WAIT_SERVIDOR:
            lista_sockets_listos = select.select([self.receiver_socekt], [], [], 0)
            if(self.Termino == True):
                return
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
                
                print("ES PAQUETE FIN")
                self.Termino = True
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
                paqueteRecibido = self.recibirAckHandshake()
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

    
    def recibirAckHandshake(self):
        timeout_start = time.time()
        while True:
                lista_sockets_listos = select.select([self.receiver_socekt], [], [], 0)
                var = time.time()
                if ((var - timeout_start) >= (MAX_WAIT)):
                        return None
                if (self.Termino == True):
                    return
                if not lista_sockets_listos[0]:
                        continue
                paqueteString, sourceAddress = self.receiver_socekt.recvfrom(2048)
                print("recibirPaquete: el string del paquete es: ", paqueteString)
                return self.gestor_paquete.pasarBytesAPaquete(paqueteString)