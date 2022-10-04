from socket import *
import time
import gestorPaquetes
import threading
import sender_server

MSJ_SIZE = 2000
MAX_WAIT = 3

class StopWait(threading.Thread,sender_server.Sender_Server):
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

    def enviar(self,mensaje):
        pck = self.gestorPaquetes.crearPaquete(mensaje)
        pckBytes = self.gestorPaquetes.pasarPaqueteABytes(pck)
        self.sender_socekt.sendto(pckBytes ,(self.receiver_ip,self.receiver_port))
        cantidad_intentos = 1
        #print("\n--El mensaje a enviar es: ", mensaje)
        print("\n-cantidad intentos es ", cantidad_intentos)

        paqueteRecibido = self.recibirPaquete()
        print("1 Paquete recibido es de tipo:",paqueteRecibido)
        
        while(paqueteRecibido == None and cantidad_intentos <= 3):
            #print("Reenvio mensaje:", mensaje)
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

  #AUXILIARES PARA ENVIAR_FINAL
    def terminar_ejecucion(self, nuevo_estado):
        self.Termino = nuevo_estado

    def recibir_y_esperar(self, pckBytes):
        cantidad_intentos = 1
        paqueteRecibido = self.recibirPaquete()
        
        while(paqueteRecibido == None and cantidad_intentos <= 3):
            self.sender_socekt.sendto(pckBytes,(self.receiver_ip,self.receiver_port))
            paqueteRecibido = self.recibirPaquete()
            if(paqueteRecibido != None): #agrego caso borde
                break
            cantidad_intentos += 1
        
        return paqueteRecibido, cantidad_intentos


 
#CREO QUE NO SE ESTÁ USANDO!
    def enviarPaquetes(self, file):

        mensaje = file.read(MSJ_SIZE)
        while(len(mensaje) > 0):
            intentar_mandar,paquete_recibido = self.enviar(mensaje)
            
            if (intentar_mandar == False):
                print(" \n intentar mandar es False, return ")
                self.Termino =  True
                return
            verificar_ack = self.gestorPaquetes.actualizarACK(paquete_recibido) #lo cambi;e a verificarACK
            print("Verificar ack es: ",verificar_ack)
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
    
