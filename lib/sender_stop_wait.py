from socket import *
import gestorPaquetes
import sender

MSJ_SIZE = 2000

MAX_TRIES = 2
BLOCKING = 1


class StopWait(sender.Sender):
    def __init__(self,server_ip,server_port,filename,filepath,logger):
        self.sender_socekt = socket(AF_INET,SOCK_DGRAM)
        self.sender_socekt.setblocking(False)
        self.receiver_ip = server_ip
        self.receiver_port = server_port
        self.filePath = filepath
        self.fileName = filename
        self.gestorPaquetes = gestorPaquetes.Gestor_Paquete()
        self.logger = logger


    def enviar(self,mensaje):
        pck = self.gestorPaquetes.crearPaquete(mensaje)
        pckBytes = self.gestorPaquetes.pasarPaqueteABytes(pck)
        self.sender_socekt.sendto(pckBytes ,(self.receiver_ip,self.receiver_port))
        cantidad_intentos = 1
        #print("\n--El mensaje a enviar es: ", mensaje)
        #print("Bytes a enviar son: ",pckBytes)
        #print("\n-cantidad intentos es ", cantidad_intentos)

        paqueteRecibido = self.recibirPaquete()
        #print("1 Paquete recibido es de tipo:",paqueteRecibido)
        
        while(paqueteRecibido == None and cantidad_intentos <= 3):
            #print("Reenvio mensaje:", mensaje)
            #entidad.enviarPaquete(pckBytes)
            self.sender_socekt.sendto(pckBytes ,(self.receiver_ip,self.receiver_port))
            paqueteRecibido = self.recibirPaquete()
            cantidad_intentos += 1
            #print("-cantidad intentos es ", cantidad_intentos)
            #print("\n El paquete recibido es de tipo ", paqueteRecibido)
            if(paqueteRecibido != None): #agrego caso 4 INTENTOS HACEMOS
                return (True,paqueteRecibido)
            ##print("\n--El mensaje a enviar es: ", mensaje)
            
            #print("\n")
        if(cantidad_intentos > 3):
            return (False,None)
        return (True,paqueteRecibido)
    
#STOP AND WAIT
    def enviarPaquetes(self, file):

        mensaje = file.read(MSJ_SIZE)
        
        while(len(mensaje) > 0):
            intentar_mandar,paquete_recibido = self.enviar(mensaje)
             
            if (intentar_mandar == False):
                #print(" \n intentar mandar es False, return ")
                return
            verificar_ack = self.gestorPaquetes.actualizarACK(paquete_recibido) #lo cambi;e a verificarACK
            intentar_mandar_ack = True
            if(verificar_ack == False): #EXTREMA SEGURIDAD --> ACK CORRUPTO
                cant_max_envios = 0
                while (cant_max_envios <= 3):
                    intentar_mandar_ack,paquete_recibido = self.enviar(mensaje)
                    cant_max_envios += 1
            if (intentar_mandar_ack == False):
                #print ("\n intentar mandar ack es False, return")
                return
            mensaje = file.read(MSJ_SIZE)
        conexion_cerrada, pck_recibido = self.enviar_fin()
        if(conexion_cerrada == True):
            print("CONEXION CERRADO CON EXITO")
        return    