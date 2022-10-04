
from socket import*
import select
import threading
import conexiones_hilo


BUFFER_RECVFROM = 2048

class Server(threading.Thread):
    def __init__(self,serverIP,serverPort,pathSave,protocolo):
        threading.Thread.__init__(self)
        self.conexiones = {}
        self.serverSocket = socket(AF_INET, SOCK_DGRAM)
        self.serverSocket.bind((serverIP,serverPort))
        self.serverSocket.setblocking(False)
        self.socket_cerrado = False
        self.numero_hilos = 0
        self.protocolo = protocolo
        self.pathSave = pathSave
        
        

    def run(self):
        while True:
            if self.socket_cerrado == True:
                return
            lista_sokcets_listos = select.select([self.serverSocket], [], [], 1)
            if not lista_sokcets_listos[0]:
                self.limpiar_conexiones_sin_usar()
                continue
            message, clientAdress = self.serverSocket.recvfrom(BUFFER_RECVFROM) #tamanio buffer para 1 paquete
            if(clientAdress not in self.conexiones): #verifico si ya existe la direccion de donde recibi el paquete
                self.conexiones[clientAdress] = conexiones_hilo.Conexion(self.numero_hilos,clientAdress,self.protocolo,self.pathSave) #guardo el hilo que se encarga de esa direccion
                self.conexiones[clientAdress].start() #inicio el hilo
                self.numero_hilos += 1
            self.conexiones[clientAdress].pasar_data(message) #le paso la data al hilo
            self.limpiar_conexiones_sin_usar
                
    
    def limpiar_conexiones_sin_usar(self):
        for conexion in self.conexiones.copy():
                if self.conexiones[conexion].esta_activa() == False:
                    print("MATO LA CONEXION")
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


    def enviarPaquete(self, mensaje):
                pass









