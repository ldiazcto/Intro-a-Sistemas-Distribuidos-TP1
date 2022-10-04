import os
from socket import *
import time
import gestorPaquetes
import threading
import sender_server

MSJ_SIZE = 2000
TAM_VENTANA = 150 #tamanio de la ventana
MAX_WAIT_GOBACKN = 5
MAX_TRIES = 3
MAX_WAIT_ACKS = 5
MAX_WAIT_FIN = 10
MAX_WAIT = 10
UPLOAD = 2

class GoBackN(threading.Thread,sender_server.Sender_Server):
    def __init__(self,receiver_ip,receiver_port,filename, filePath):
        threading.Thread.__init__(self)
        self.sender_socekt = socket(AF_INET,SOCK_DGRAM)
        self.sender_socekt.setblocking(False)
        self.receiver_ip = receiver_ip
        self.receiver_port = receiver_port
        self.gestorPaquetes = gestorPaquetes.Gestor_Paquete()
        self.cola = []
        self.filename = filename
        self.hay_data = False
        self.older_seq_number = 1
        self.new_seq_number = 0
        self.paquetesEnVuelo = []
        self.Termino = False
        self.filePath = filePath



    def run(self):
        self.enviar_archivo()


    def enviarPaquetes(self,file):
        mensaje = "entrar en ciclo"
        timeout_start = 0
        while (True):
            
            #si el numero de sequencia del siguiente paquete a enviar es menor al numero de seq del primer paquete que envie
            # -- ENVIAR ACK --
            if(self.new_seq_number < self.older_seq_number + TAM_VENTANA):
                mensaje = file.read(MSJ_SIZE)
                if(len(mensaje) != 0):
                    pck = self.gestorPaquetes.crearPaquete(mensaje)
                    self.paquetesEnVuelo.append(pck)
                    
                    self.sender_socekt.sendto(self.gestorPaquetes.pasarPaqueteABytes(pck),(self.receiver_ip,self.receiver_port))
                    #print ("Envio Mensaje: ",self.gestorPaquetes.pasarPaqueteABytes(pck))
                    self.new_seq_number = pck.obtenerSeqNumber()
                    if(self.older_seq_number == self.new_seq_number): #entrás cuando corriste la ventana entera
                        timeout_start = time.time()    
                    #self.new_seq_number += 1  
                    continue
                
            if(len(self.paquetesEnVuelo) == 0):
                break
            #print("ME QUEDO DANDO VUELTAS")
            #-- IMPLEMENTACION FEDE
            pckRecibido, esACKEsperado = self.recibirPaqueteACK()
            #print(esACKEsperado)
            #if(len(self.paquetesEnVuelo) == TAM_VENTANA and esACKEsperado == False):
                #continu

            # -- VERIFICACION DE ACK --
            if (esACKEsperado) : #SI RECIBO UN ACK, SIGNIFICA QUE RECIBI EL ACK DEL ULTIMO PAQUETE QUE LLEGO BIEN
                                        # (ES DECIR QUE, TODOS LOS PAQUETES ANTERIORES TMB LLEGARON BIEN)
                #muevo el older_seq_number a la posicion siguiente al new_seq_number
                #print("ACK CORRECTO")
                cant_paquetes_a_popear =  pckRecibido.obtenerSeqNumber() - self.older_seq_number 
                self.older_seq_number = pckRecibido.obtenerSeqNumber()+1
                #print("DIFERENCIA ES: ",cant_paquetes_a_popear)
                for i in range(cant_paquetes_a_popear + 1 ): 
                    pck = self.paquetesEnVuelo.pop(0) #borro el paquete que llego bien (voy borrando de a uno)
                    #print("SEQ NUMBER POPEADO ES: ",pck.obtenerSeqNumber())
                if(self.older_seq_number == self.new_seq_number):
                    #STOP_TIMER QUE SERA ???
                    #print("STOP TIMER")
                    break
                else:    
                    timeout_start = time.time() #reinicio el timer porque los paquetes me llegaron bien, corro el older porque tengo que mandar paquetes nuevos 
                
                    

            # -- REENVIAR PCKS EN CASO DE ERROR --
            var = time.time()
            saltoTimerReenvio = (var - timeout_start)  >= MAX_WAIT_GOBACKN
            ###print("TIMEOUT START ES:",timeout_start)
            ##print(var - timeout_start)
            if(saltoTimerReenvio and timeout_start != 0): #SI SALTO TIMEOUT, ENTONCES PERDI UN PAQUETE Y POR ENDE TENGO 
                                                            #QUE VOLVER A INICIAR EL TIMER Y ENVIAR LOS PAQUETES QUE ME QUEDARON EN LA LISTA DE PAQUETES EN VUELO
                #print("\n\n SALTO EL TIMER \n\n")
                timeout_start = time.time()
                for pck in self.paquetesEnVuelo:
                    self.sender_socekt.sendto(self.gestorPaquetes.pasarPaqueteABytes(pck),(self.receiver_ip,self.receiver_port))
        #print("Cantidad paquetes en vuelo: ", len(self.paquetesEnVuelo))
        conexion_cerrada,pck_recibido = self.enviar_fin()
        if(conexion_cerrada == True):
            print("CONEXION CERRADO CON EXITO")
        self.Termino = True
        return

#AUXILIARES HANDSHAKE

    def entablarHandshake(self, fileName, fileSize):
        paquete = self.crearPaqueteHandshake_upload(fileName, fileSize)
        paqueteBytes = self.gestorPaquetes.pasarPaqueteABytes(paquete)
        i = 0
        while i <= MAX_TRIES:
                self.sender_socekt.sendto(paqueteBytes,(self.receiver_ip,self.receiver_port))
                paqueteRecibido = self.recibirPaquete()
                #TIMEOUTEA VUELVO A ENVIAR EL HANDSHAKE
                if (paqueteRecibido == None):
                        #print(i)
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


    def crearPaqueteHandshake_upload(self, fileName, fileSize):
        caracterSeparador = "-"
        mensaje = fileName
        mensaje = mensaje + caracterSeparador + str(fileSize)
        return self.gestorPaquetes.crearPaqueteHandshake(UPLOAD, mensaje)


 #AUXILIARES RECIBIR PAQUETES
    
    def recibirPaqueteACK(self) :
        pckRecibido = self.recibirPaqueteBackN() #obtengo el ultimo paquete recibido
        ackRecibido = self.gestorPaquetes.actualizarACK(pckRecibido)
        return pckRecibido, ackRecibido
    

    def recibirPaqueteBackN(self):
        if (self.hay_data == False):
            return None
        paqueteString = self.cola.pop(0)
        if(len(self.cola) == 0):
            self.hay_data = False
        #print("recibirPaquete: el string del paquete es: ", paqueteString)
        return self.gestorPaquetes.pasarBytesAPaquete(paqueteString)


 
    #AUXILIARES PARA ENVIAR_FINAL
    def terminar_ejecucion(self, nuevo_estado):
        return

    def recibir_y_esperar(self, pckBytes):
        cantidad_intentos = 1
        paqueteRecibido = self.recibirPaquete()
        while(paqueteRecibido == None and cantidad_intentos <= 3):

            paqueteRecibido = self.recibirPaquete()
            cantidad_intentos += 1
        return paqueteRecibido, cantidad_intentos
    



