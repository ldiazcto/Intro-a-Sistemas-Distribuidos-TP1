import os
from socket import *
import time
import enviador
import gestorPaquetes
import threading

MSJ_SIZE = 10
UPLOAD = 2
MAX_TRIES = 2
MAX_WAIT = 10
NOT_BLOCKING= 0 
BLOCKING = 1
MAX_WAIT_RESPONSE = 10
import select

class StopWait(threading.Thread):
    def __init__(self,receiver_ip,receiver_port,filename,filePath):
        threading.Thread.__init__(self)
        self.sender_socekt = socket(AF_INET,SOCK_DGRAM)
        self.sender_socekt.setblocking(False)
        self.receiver_ip = receiver_ip
        self.receiver_port = receiver_port
        self.gestorPaquetes = gestorPaquetes.Gestor_Paquete()
        self.cola = []
        self.filename = filename
        self.hay_data = False
        self.Termino = False
        self.filePath = filePath

    def run(self):
        self.enviar_archivo()

    def pasar_data(self, paquete= b""):
        self.cola.append(paquete)
        self.hay_data = True

    def enviar_archivo(self):
        #filepath= self.filePath + self.filename
        print("Path de archivos",self.filePath)
        #file_stats = os.stat(self.filePath)
        #file_size = file_stats.st_size
        file = open(self.filePath,'rb')
        self.enviarPaquetes(file)
        self.Termino = True
        file.close()



    def enviar(self,mensaje):
        pck = self.gestorPaquetes.crearPaquete(mensaje)
        pckBytes = self.gestorPaquetes.pasarPaqueteABytes(pck)
        #entidad.enviarPaquete(pckBytes)
        self.sender_socekt.sendto(pckBytes ,(self.receiver_ip,self.receiver_port))
        cantidad_intentos = 1
        print("\n--El mensaje a enviar es: ", mensaje)
        print("\n-cantidad intentos es ", cantidad_intentos)

        paqueteRecibido = self.recibirPaquete()
        print("1 Paquete recibido es de tipo:",paqueteRecibido)
        
        while(paqueteRecibido == None and cantidad_intentos <= 3):
            print("Reenvio mensaje:", mensaje)
            #entidad.enviarPaquete(pckBytes)
            self.sender_socekt.sendto(pckBytes ,(self.receiver_ip,self.receiver_port))
            paqueteRecibido = self.recibirPaquete()
            cantidad_intentos += 1
            print("\n El paquete recibido es de tipo ", paqueteRecibido)
            if(paqueteRecibido != None): #agrego caso 4 INTENTOS HACEMOS
                return (True,paqueteRecibido)
            #print("\n--El mensaje a enviar es: ", mensaje)
            print("-cantidad intentos es ", cantidad_intentos)
            print("\n")
        if(cantidad_intentos > 3):
            self.Termino = True
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
            self.Termino = True
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
                self.Termino =  True
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
                self.Termino =  True
                return
            mensaje = file.read(MSJ_SIZE)
        conexion_cerrada,pck_recibido = self.enviar_fin()
        if(conexion_cerrada == True):
            print("CONEXION CERRADO CON EXITO")
            self.Termino = True
        return
    

    def recibirPaquete(self):
        timeout_start = time.time()
        while True:
                """"
                lista_sockets_listos = select.select([self.sender_socekt], [], [], 0)
                var = time.time()
                if ((var - timeout_start) >= (MAX_WAIT)):
                        return None
                if not lista_sockets_listos[0]:
                        continue
                """
                var = time.time()
                if ((var - timeout_start) >= (MAX_WAIT)):
                        return None
                if (self.hay_data == False):
                    continue
                paqueteString = self.cola.pop(0)
                if(len(self.cola) == 0):
                    self.hay_data = False
                print("recibirPaquete: el string del paquete es: ", paqueteString)
                return self.gestorPaquetes.pasarBytesAPaquete(paqueteString)

