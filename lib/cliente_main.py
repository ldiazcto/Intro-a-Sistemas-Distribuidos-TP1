import cliente, stopAndWait, goBackN #nombre del archivo
import getopt
import sys

SERVER_ADDR = ""
SERVER_PORT = 120
FILEPATH = ""
FILENAME = ""
MAX_FILE_SIZE = 30
UPLOAD = 2
DOWNLOAD = 3

def abrirArchivo(ruta):
        try:
            file = open(ruta,'rb')
            return file
        except FileNotFoundError: #o IOERROR o FileExistsError
            print("FILE NO ENCONTRADO")
            sys.exit(2)

def cerrarArchivo(file):
    file.close()



# def obtenerArgumentos():
#     opcionesCortas = "hvqH:p:s:n:d:" #se utilizan con -. 
#     opcionesLargas = ["help","verbose","quiet","host=","port=","src=","name=","dst="] #se utilizan con --

#     listaArgumentos = sys.argv[1:]
#     try:
#         return getopt.getopt(listaArgumentos,opcionesCortas,opcionesLargas) #par tuplas
#     except getopt.error as err:
#         print(str(err))
#         sys.exit(2)   #conexion muerta


# def definirVerbosidad(opt):
#     verbosity = 0
#     if ((opt in ('-v','--verbose')) and opt in (('-q','--quiet'))):
#         print("Se pide alta y baja verbosidad a la vez. Por favor, elegir uno o ninguno.")
#         sys.exit(0)
        
#     if(opt in ('-v','--verbose')):
#         verbosity += 1
#         if(verbosity >= 3):
#            logging.debug()
                    
#     if (opt in ('-q','--quiet')):
#         verbosity -= 1
#         if(verbosity < 0):
#           logging.warning()     



# def definirPuertoYNombre(opt, arg):
#     if(opt in ('-p','--port')):
#         SERVER_PORT = arg
#         #puerto del servidor
                    
#     if(opt in ('-n','--name')):
#         FILENAME = arg
#         #nombre del paquete


def main():
   
    cliente_prueba = cliente.Cliente("localhost", 12000)
    #stopWait = stopAndWait.StopAndWait()
    backN = goBackN.GoBackN() #llamo a la clase, y me ejecuta el constructor
    print("Se creo el cliente con exito")
    file = abrirArchivo("./lib/hola.txt")
    cliente_prueba.enviarArchivo(file,backN)
    return 0
    
    # opciones, argumentos = obtenerArgumentos()

    # for opt,arg in opciones: #para entrar en las tuplas de opciones y analizar
    #     try:
    #         if(sys.argv[0] == "upload" or sys.argv[0] == "download"):
    #             if (opt in ('-h','--help')):
    #                 #mostrar mensaje de ayuda
    #                 print("Preguntamos qué hace acá por slack")
    #                 sys.exit(0) #salir con exito

    #             definirVerbosidad(opt)

    #             if (opt in ('-H','--host')):
    #                 SERVER_ADDR = arg
    #                 #direccion IP del servidor

    #             definirPuertoYNombre(opt, arg)

    #             #cliente se inicializa
    #             client = cliente(SERVER_ADDR, SERVER_PORT)
    #             stopWait = stopAndWait.StopAndWait()
    #             backN = goBackN.GoBackN()
    #             protocolo = input("Elegir protocolo (S/G): \n")
    #             seguir = True
    #             while(seguir):
    #                 #backN = goBackN.GoBackN() #llamo a la clase, y me ejecuta el constructor
    #                 if(protocolo == "S" or protocolo == "s"):
    #                     if(sys.argv[0] == "upload"):
    #                         if(opt in ('-s','--src')):
    #                             FILEPATH = arg
    #                             #ruta de origen del paquete
    #                             client.enviarArchivo(FILEPATH,stopWait)
    #                     if(sys.argv[0] == "download"):
    #                         if(opt in ('-d','--dst')):
    #                             print("No está implementado")
    #                             FILEPATH = arg
    #                             #ruta de destino del paquete
    #                             #cliente.recibirArchivo(FILEPATH)
    #                 elif(protocolo == "G" or protocolo == "g"):
    #                     if(sys.argv[0] == "upload"):
    #                         if(opt in ('-s','--src')): #esto no debería ser un if, este valor debería estar
    #                             FILEPATH = arg

#                             fileSize = os.stat(FILEPATH).st_size
#                             if fileSize > MAX_FILE_SIZE:
#                                   print("El tamaño del archivo excede los límites posibles. El máximo es " + MAX_FILE_SIZE + " en bytes.")
#                                   sys.exit(2)

#                             file = self.abrirArchivo(FILEPATH)
#                             handshakeExitoso = cliente.entablarHandshake(FILENAME, tamanio_archivo, UPLOAD)
#                             if (not handshakeExitoso) :
#                                   return
#                             client.enviarArchivo(FILEPATH,backN)
#                             self.cerrarArchivo(file)
    #                     if(sys.argv[0] == "download"):
    #                         if(opt in ('-d','--dst')):
    #                             FILEPATH = arg #ruta donde guardo el archivo
    #                             handshakeExitoso = cliente.entablarHandshake(FILENAME, 0, DOWNLOAD)
    #                             if (not handshakeExitoso) :
#                                      return
    #                             
    #                              #file = cliente.recibirArchivo(FILEPATH, FILENAME)
    #                               self.cerrarArchivo(file)
    # 
    # 
    # 
    # 
    #                 cambiarModo = input("Quiere cambiar de protocolo? S/N: \n")
    #                 if(cambiarModo == "N"):
    #                     seguir = False
    #                 elif(cambiarModo == "S"):
    #                     protocolo = input("Elegir protocolo (S/G): \n")
    #                     seguir = True
    #                 else:
    #                     return
    #         sys.exit(0)

    #     except sys.argv[0] != "upload" and sys.argv[0] != "download": #agregar except para no sourcfile y no sourcename ni destination port
    #         print(" -- DEAD CONNECTION --")
    #         sys.exit(2)

main()