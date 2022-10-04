from socket import *
import time
import gestorPaquetes
import select
import sender

MSJ_SIZE = 2000
MAX_WAIT = 10

BLOCKING = 1

TAM_VENTANA = 150
MAX_WAIT_GOBACKN = 5

class GoBackN(sender.Sender):
    def __init__(self,server_ip,server_port,filename,filepath):
        self.sender_socekt = socket(AF_INET,SOCK_DGRAM)
        self.sender_socekt.setblocking(False)
        self.receiver_ip = server_ip
        self.receiver_port = server_port
        self.gestorPaquetes = gestorPaquetes.Gestor_Paquete()
        self.older_seq_number = 1
        self.new_seq_number = 0
        self.paquetesEnVuelo = []
        self.filePath = filepath
        self.fileName = filename


    def recibirPaqueteACK(self) :
        pckRecibido = self.recibirPaqueteBackN() #obtengo el ultimo paquete recibido
        ackRecibido = self.gestorPaquetes.actualizarACK(pckRecibido)
        return pckRecibido, ackRecibido
    

    def recibirPaqueteBackN(self):
                lista_sockets_listos = select.select([self.sender_socekt], [], [], 0)
                if not lista_sockets_listos[0]:
                        return None
                paqueteString, sourceAddress = self.sender_socekt.recvfrom(2048)
                #print("recibirPaquete: el string del paquete es: ", paqueteString)
                return self.gestorPaquetes.pasarBytesAPaquete(paqueteString)


    def enviarPaquetes(self,file):
            mensaje = "entrar en ciclo"
            timeout_start = 0
            cantidad_intentos = 0
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
                    
                #-- IMPLEMENTACION FEDE
                pckRecibido, esACKEsperado = self.recibirPaqueteACK()

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
                        break
                    else: 
                        cantidad_intentos = 0   
                        timeout_start = time.time() #reinicio el timer porque los paquetes me llegaron bien, corro el older porque tengo que mandar paquetes nuevos 
                    
                if(cantidad_intentos >= 3):
                    break
                # -- REENVIAR PCKS EN CASO DE ERROR --
                var = time.time()
                saltoTimerReenvio = (var - timeout_start)  >= MAX_WAIT_GOBACKN
                ##print("TIMEOUT START ES:",timeout_start)
                ##print(var - timeout_start)
                if(saltoTimerReenvio and timeout_start != 0): #SI SALTO TIMEOUT, ENTONCES PERDI UN PAQUETE Y POR ENDE TENGO 
                                                                #QUE VOLVER A INICIAR EL TIMER Y ENVIAR LOS PAQUETES QUE ME QUEDARON EN LA LISTA DE PAQUETES EN VUELO
                    cantidad_intentos +=1
                    #print("\n\n SALTO EL TIMER \n\n")
                    timeout_start = time.time()
                    for pck in self.paquetesEnVuelo:
                        self.sender_socekt.sendto(self.gestorPaquetes.pasarPaqueteABytes(pck),(self.receiver_ip,self.receiver_port))
            #print("Cantidad paquetes en vuelo: ", len(self.paquetesEnVuelo))
            conexion_cerrada, pck_recibido = self.enviar_fin()
            if(conexion_cerrada == True):
                print("CONEXION CERRADO CON EXITO")
            return



    



