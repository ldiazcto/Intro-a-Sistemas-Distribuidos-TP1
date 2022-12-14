from socket import *
import time
import gestorPaquetes
import select
import sender

class GoBackN(sender.Sender):
    def __init__(self,server_ip,server_port,filename,filepath,logger):
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
        self.logger = logger
        self.MSJ_SIZE = 2000
        self.MAX_TRIES = 3
        self.MAX_WAIT = 10
        self.MAX_WAIT_GOBACKN = 5
        self.TAM_VENTANA = 150
        self.UPLOAD = 2
        self.CARACTER_SEPARADOR = "-"

    def recibirPaqueteACK(self) :
        pckRecibido = self.recibirPaqueteBackN()
        ackRecibido = self.gestorPaquetes.actualizarACK(pckRecibido)
        return pckRecibido, ackRecibido
    

    def recibirPaqueteBackN(self):
                lista_sockets_listos = select.select([self.sender_socekt], [], [], 0)
                if not lista_sockets_listos[0]:
                        return None
                paqueteString, sourceAddress = self.sender_socekt.recvfrom(2048)
                
                return self.gestorPaquetes.pasarBytesAPaquete(paqueteString)


    def enviarPaquetes(self,file):
            mensaje = "entrar en ciclo"
            timeout_start = 0
            cantidad_intentos = 0
            self.logger.debug("A punto de comenzar el loop par enviar paquetes en Go Back N...")
        
            while (True):
                self.logger.debug(f"La ventana va de {self.older_seq_number} a {self.older_seq_number + self.TAM_VENTANA} y el sequence number actual es {self.new_seq_number}")
                if(self.new_seq_number < self.older_seq_number + self.TAM_VENTANA):
                    mensaje = file.read(self.MSJ_SIZE)
                    if(len(mensaje) != 0):
                        pck = self.gestorPaquetes.crearPaquete(mensaje)
                        self.paquetesEnVuelo.append(pck)
                        
                        self.sender_socekt.sendto(self.gestorPaquetes.pasarPaqueteABytes(pck),(self.receiver_ip,self.receiver_port))
                        self.new_seq_number = pck.obtenerSeqNumber()
                        if(self.older_seq_number == self.new_seq_number):
                            self.logger.debug("??? Se reinicia el timer")
                            timeout_start = time.time()     
                        continue
                pckRecibido, esACKEsperado = self.recibirPaqueteACK()
                if (esACKEsperado) :
                    self.logger.debug("??? Se recibi?? ACK esperado")
                    cant_paquetes_a_popear =  pckRecibido.obtenerSeqNumber() - self.older_seq_number 
                    self.older_seq_number = pckRecibido.obtenerSeqNumber()+1
                    for i in range(cant_paquetes_a_popear + 1 ): 
                        pck = self.paquetesEnVuelo.pop(0) 
                    if(self.older_seq_number == self.new_seq_number):
                        break
                    else: 
                        cantidad_intentos = 0   
                        timeout_start = time.time()
                if(cantidad_intentos >= self.MAX_TRIES):
                    break
                var = time.time()
                saltoTimerReenvio = (var - timeout_start)  >= self.MAX_WAIT_GOBACKN
                if(saltoTimerReenvio and timeout_start != 0):
                    cantidad_intentos +=1
                    timeout_start = time.time()
                    for pck in self.paquetesEnVuelo:
                        self.sender_socekt.sendto(self.gestorPaquetes.pasarPaqueteABytes(pck),(self.receiver_ip,self.receiver_port))
            conexion_cerrada, pck_recibido = self.enviar_fin()
            if(conexion_cerrada == True):
                self.logger.info("??? Se han enviado todos los paquetes con Go Back N y se ha cerrado la conexion con exito")
            return



    



