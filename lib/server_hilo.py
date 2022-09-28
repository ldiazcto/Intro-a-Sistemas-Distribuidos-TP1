
from socket import*
import select
import threading
import entidad
import conexiones_hilo




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

    def cerrar_socket(self):
        self.socket_cerrado = True

    def finalizar(self):
        for conexion in self.conexiones.copy():
            #PREGUNTA
            #capaz que hay que mandar un mensaje avisando a los clientes pero NO SE
            self.conexiones[conexion].join() #joineo todos los hilos
            self.conexiones.pop(conexion)
        print("DO SOMETHING")

    def recibirPaquete(self):
                #pensarla, para descargar paquetes
                return
    

    def enviarPaquete(self, mensaje):
                pass









