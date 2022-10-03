import os
from socket import *
import time
import enviador
import gestorPaquetes

MSJ_SIZE = 15
UPLOAD = 2
MAX_TRIES = 2
MAX_WAIT = 10
NOT_BLOCKING= 0 
BLOCKING = 1
MAX_WAIT_RESPONSE = 10
import select

class StopWait():
    def __init__(self,sender_ip,sender_port,receiver_ip,receiver_port):
        self.sender_socekt = socket(AF_INET,SOCK_DGRAM)
        self.sender_socekt.bind((sender_ip,sender_port)) #''  es para que escuche a todos --- serverPort es por d'onde escucha el server
        self.sender_socekt.setblocking(False)
        self.sender_ip = sender_ip
        self.sender_port = sender_port
        self.receiver_ip = receiver_ip
        self.receiver_port = receiver_port
        self.gestorPaquetes = gestorPaquetes.Gestor_Paquete()

    def enviar_archivo(self,filename):
        path = os.getcwd()
        new_path = path + "/lib"
        #print("Path de archivos",new_path)
        filepath= new_path + "/" + "hola_2.txt"
        file_stats = os.stat(filepath)
        file_size = file_stats.st_size
        handshake_establecido = self.entablarHandshake("hola.txt",file_size)
        if(handshake_establecido):
            file = open(filepath,'rb')
            self.enviarPaquetes(file)
            file.close()
        else:
            print("FALLO EL HANDSHAKE")
            return



    def enviar(self,mensaje):
        pck = self.gestorPaquetes.crearPaquete(mensaje)
        pckBytes = self.gestorPaquetes.pasarPaqueteABytes(pck)
        #entidad.enviarPaquete(pckBytes)
        self.sender_socekt.sendto(pckBytes ,(self.receiver_ip,self.receiver_port))
        cantidad_intentos = 1
        print("\n--El mensaje a enviar es: ", mensaje)
        print("Bytes a enviar son: ",pckBytes)
        print("\n-cantidad intentos es ", cantidad_intentos)

        paqueteRecibido = self.recibirPaquete()
        print("1 Paquete recibido es de tipo:",paqueteRecibido)
        
        while(paqueteRecibido == None and cantidad_intentos <= 3):
            print("Reenvio mensaje:", mensaje)
            #entidad.enviarPaquete(pckBytes)
            self.sender_socekt.sendto(pckBytes ,(self.receiver_ip,self.receiver_port))
            paqueteRecibido = self.recibirPaquete()
            cantidad_intentos += 1
            print("-cantidad intentos es ", cantidad_intentos)
            print("\n El paquete recibido es de tipo ", paqueteRecibido)
            if(paqueteRecibido != None): #agrego caso 4 INTENTOS HACEMOS
                return (True,paqueteRecibido)
            #print("\n--El mensaje a enviar es: ", mensaje)
            
            print("\n")
        if(cantidad_intentos > 3):
            return (False,None)
        return (True,paqueteRecibido)
    
    def enviar_fin(self,):
        pck = self.gestorPaquetes.crearPaqueteFin()
        pckBytes = self.gestorPaquetes.pasarPaqueteABytes(pck)
        self.sender_socekt.sendto(pckBytes,(self.receiver_ip,self.receiver_port))
        #entidad.enviarPaquete(pckBytes)
        cantidad_intentos = 1
        print("\n--El mensaje a enviar es: ", "FIN")
        print("\n-cantidad intentos es ", cantidad_intentos)

        paqueteRecibido = self.recibirPaquete()
        
        while(paqueteRecibido == None and cantidad_intentos <= 3):
            
            #entidad.enviarPaquete(pckBytes)
            self.sender_socekt.sendto(pckBytes,(self.receiver_ip,self.receiver_port))
            paqueteRecibido = self.recibirPaquete()
            print("\n\n El paquete recibido es de tipo ", paqueteRecibido)
            if(paqueteRecibido != None): #agrego caso borde
                break
            cantidad_intentos += 1
            print("\n--El mensaje a enviar es: ", "FIN")
            print("\n-cantidad intentos es ", cantidad_intentos)
        if(cantidad_intentos > 3):
            return (False,None)
        return (True,paqueteRecibido)



#STOP AND WAIT
    def enviarPaquetes(self, file):

        mensaje = file.read(MSJ_SIZE)
        
        while(len(mensaje) > 0):
            #de mensaje a paquete
            intentar_mandar,paquete_recibido = self.enviar(mensaje)
            #chequear si llego un ack
            #si llego un ack, verificar que es el correcto
            #si no llego un ack o no es el correcto, -> reenvío
            #si salta el timer, -> reenvío
            #estoy dispuesta a reenviar MAX_TRIES
            
            if (intentar_mandar == False):
                print(" \n intentar mandar es False, return ")
                return
            verificar_ack = self.gestorPaquetes.actualizarACK(paquete_recibido) #lo cambi;e a verificarACK
            intentar_mandar_ack = True
            if(verificar_ack == False): #EXTREMA SEGURIDAD --> ACK CORRUPTO
                cant_max_envios = 0
                while (cant_max_envios <= 3):
                    intentar_mandar_ack,paquete_recibido = self.enviar(mensaje)
                    cant_max_envios += 1
            if (intentar_mandar_ack == False):
                print ("\n intentar mandar ack es False, return")
                return
            mensaje = file.read(MSJ_SIZE)
        conexion_cerrada,pck_recibido = self.enviar_fin()
        if(conexion_cerrada == True):
            print("CONEXION CERRADO CON EXITO")
        return
    

    def recibirPaquete(self):
        timeout_start = time.time()
        while True:
                lista_sockets_listos = select.select([self.sender_socekt], [], [], 0)
                var = time.time()
                if ((var - timeout_start) >= (MAX_WAIT)):
                        return None
                if not lista_sockets_listos[0]:
                        continue
                paqueteString, sourceAddress = self.sender_socekt.recvfrom(2048)
                print("recibirPaquete: el string del paquete es: ", paqueteString)
                return self.gestorPaquetes.pasarBytesAPaquete(paqueteString)


    def crearPaqueteHandshake_upload(self, fileName, fileSize):
        caracterSeparador = "-"
        mensaje = fileName
        mensaje = mensaje + caracterSeparador + str(fileSize)
        return self.gestorPaquetes.crearPaqueteHandshake(UPLOAD, mensaje)



    def entablarHandshake(self, fileName, fileSize):
                paquete = self.crearPaqueteHandshake_upload(fileName, fileSize)
                paqueteBytes = self.gestorPaquetes.pasarPaqueteABytes(paquete)
                i = 0
                while i <= MAX_TRIES:
                        self.sender_socekt.sendto(paqueteBytes,(self.receiver_ip,self.receiver_port))
                        paqueteRecibido = self.recibirPaquete()
                        #TIMEOUTEA VUELVO A ENVIAR EL HANDSHAKE
                        if (paqueteRecibido == None):
                                print(i)
                                i += 1
                                continue
                        esPaqueteOrdenado = self.gestorPaquetes.verificarACK(paqueteRecibido)
                        if (esPaqueteOrdenado) :
                                return True
                        esPaqueteRefused = self.gestorPaquetes.verificarRefused(paqueteRecibido)
                        if (esPaqueteRefused) :
                                return False
                        i +=1

                return False
    


    