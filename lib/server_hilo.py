
from socket import*
import select
import threading
import time
import entidad
import conexiones_hilo
import gestorPaquetes

MAX_WAIT_HANDSHAKE = 30
MAX_TAMANIO_PERMITIDO = 30 #en bytes

class Server(threading.Thread,entidad.Entidad):
    def __init__(self):
        threading.Thread.__init__(self)
        entidad.Entidad.__init__(self,'',12000)
        self.conexiones = {}
        serverPort = 12000
        self.serverSocket = socket(AF_INET, SOCK_DGRAM)
        self.serverSocket.bind(('',serverPort))
        self.serverSocket.setblocking(False)
        self.socket_cerrado = False
        self.numero_hilos = 0
        
        

    def run(self):
        while True:
            if self.socket_cerrado == True:
                return
            lista_sokcets_listos = select.select([self.serverSocket], [], [], 1)
            if not lista_sokcets_listos[0]:
                continue
            message, clientAdress = self.serverSocket.recvfrom(2048) #tamanio buffer para 1 paquete
            print ("El mensaje recibido es: ",message)
            #modifiedMessage = message.decode() #decoder paquete
            if(clientAdress not in self.conexiones): #verifico si ya existe la direccion de donde recibi el paquete
                self.conexiones[clientAdress] = conexiones_hilo.Conexion(self.numero_hilos,clientAdress) #guardo el hilo que se encarga de esa direccion
                self.conexiones[clientAdress].start() #inicio el hilo
                self.numero_hilos += 1
            self.conexiones[clientAdress].pasar_data(message) #le paso la data al hilo
            for conexion in self.conexiones.copy():
                if self.conexiones[conexion].esta_activa() == False:
                   self.conexiones[conexion].join() 
                   self.conexiones.pop(conexion)   

    def chequearHandshakeApropiado(paquete):
        return (paquete.esDownload() or paquete.esUpload())

    def obtenerTamanio(mensaje):
        nombre, tamanio = mensaje.split("-")
        return tamanio

    def chequearTamanio(self, paquete) :
        if paquete.esDownload() :
            return True
        
        tamanio = self.obtenerTamanio(paquete.obtenerMensaje())
        if (tamanio >= MAX_TAMANIO_PERMITIDO):
            return False
        return True

    def esHandshakeUpload(paquete):
        return paquete.esUpload()

    def enviarACKHandshake(self):
        #crear paquete
        gP = gestorPaquetes.Gestor_Paquete()
        pck = gP.crearPaqueteACK()
        
        #pasarlo a bytes
        pckBytes = gP.pasarPaqueteABytes(pck)

        #pasarlo con enviarPaquete 
        self.enviarPaquete(pckBytes)

    def recibirHandshake(self):
        time_start = time.time()
        paqueteRecibido = None
        while time.time() < time_start + MAX_WAIT_HANDSHAKE and paqueteRecibido == None:
                paqueteRecibido = self.recibirPaquete()
        
        if (paqueteRecibido == None) :
            print("Salto el timer, me voy")
            return None
        
        return paqueteRecibido
            
                
                

    def cerrar_socket(self):
        self.socket_cerrado = True

    def finalizar(self):
        for conexion in self.conexiones.copy():
            #PREGUNTA
            #capaz que hay que mandar un mensaje avisando a los clientes pero NO SE
            self.conexiones[conexion].join() #joineo todos los hilos
            self.conexiones.pop(conexion)
        print("DO SOMETHING")


    def enviarPaquete(self, mensaje):
                pass









