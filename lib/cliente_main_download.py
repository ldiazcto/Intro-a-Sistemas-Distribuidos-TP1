import os
import cliente, stopAndWait, goBackN #nombre del archivo
import getopt
import sys
import logging
import gestorPaquetes
import sender_stop_wait
import sender_gobackn
import receiver

SERVER_ADDR = ""
SERVER_PORT = 120
FILEPATH = ""
FILENAME = ""
UPLOAD = 2
DOWNLOAD = 3

#NIVELES DE LOGS
NOTSET = 0
DEBUG = 10
INFO = 20
WARNING = 30
CRITICAL = 50
QUIET = 51

def abrirArchivo(ruta):
        try:
            file = open(ruta,'rb')
            return file
        except FileNotFoundError: #o IOERROR o FileExistsError
            print("FILE NO ENCONTRADO")
            sys.exit(2)

# def cerrarArchivo(file):
#     file.close()



# def obtenerArgumentos():
#     opcionesCortas = "hvqH:p:s:n:d:" #se utilizan con -. 
#     opcionesLargas = ["help","verbose","quiet","host=","port=","src=","name=","dst="] #se utilizan con --

#     listaArgumentos = sys.argv[1:]
#     print(listaArgumentos)
#     try:
#         return getopt.getopt(listaArgumentos,opcionesCortas,opcionesLargas) #par tuplas
#     except getopt.error as err:
#         print(str(err))
#         sys.exit(2)   #conexion muerta


# def definirVerbosidad(opt, logger):
#     #Para definir la verbosidad, le tengo que setear el nivel al logger, dependiendo lo que quiero mostrar 
#     verbosity = 0
#     if ((opt in ('-v','--verbose')) and opt in (('-q','--quiet'))):
#         print("Se pide alta y baja verbosidad a la vez. Por favor, elegir uno o ninguno.")
#         sys.exit(0)

#
# q = 0
# nada por default 1
# v = 2 

#     if(opt in ('-v','--verbose')):
#         verbosity += 1
#         logger.setLevel()           
#
#         if(verbosity >= 3):
#            logger.setLevel(logging.DEBUG)
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
    """
    file_handler = logging.FileHandler(filename='tmp.log')
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    handlers = [file_handler, stdout_handler]

    logging.basicConfig(
        level=logging.DEBUG, 
        format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
        handlers=handlers
    )
    
    logger = logging.getLogger()
    
    logger.info("Se inicio el logger")
    """

    receiver_aux = receiver.Receiver("localhost", 8080,"localhost", 12000, "/Users/abrildiazmiguez/Desktop/Intro_a_Distr/Intro-a-Sistemas-Distribuidos-TP1/lib/BDD_Cliente")
    receiver_aux.recibir_archivo("lp_desde_servidor.pdf")
    """
    cliente_prueba = cliente.Cliente("localhost", 8090, 12000, logger) #los dos puertos del cliente son 8080 y el server escucha del 12000
    stopWait = stopAndWait.StopAndWait()
    backN = goBackN.GoBackN() #llamo a la clase, y me ejecuta el constructor
    print("Se creo el cliente con exito")

    ruta = "/home/fede/Desktop/distribuidos/alternativa/Intro-a-Sistemas-Distribuidos-TP1/lib/foto_prueba.png"
    file_name = "nueva_foto_prueba_6_GBN.png"
    ruta2 = "/home/fede/Desktop/distribuidos/alternativa/Intro-a-Sistemas-Distribuidos-TP1/lib/hola2.txt"
    
    #file_size = os.path.getsize(ruta)
    #print("El tam de mi archivo es: ", file_size)

    resultado = cliente_prueba.entablarHandshake(file_name, 166997, UPLOAD)
    print("----------------------------El resultado de mi handshake es: ", resultado)
    
    file = abrirArchivo(ruta)
    if resultado == True : cliente_prueba.enviarArchivo(file,backN)
    return 0
    """
main()
    # opciones, argumentos = obtenerArgumentos()
    # print("OPCIONES: ",opciones)
    # for opt,arg in opciones: #para entrar en las tuplas de opciones y analizar
    #     try:
    #         print("Elegi mis opciones: ", opt)
    #         if(sys.argv[0] == "upload" or sys.argv[0] == "download"):
    #             if (opt in ('-h','--help')):
    #                 #mostrar mensaje de ayuda
    #                 print("Preguntamos qué hace acá por slack")
    #                 sys.exit(0) #salir con exito

    #             definirVerbosidad(opt, logger)

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
                            
                            
    #                         fileSize = os.stat(FILEPATH).st_size
    #                         if fileSize > MAX_FILE_SIZE:
    #                               print("El tamaño del archivo excede los límites posibles. El máximo es " + MAX_FILE_SIZE + " en bytes.")
    #                               sys.exit(2)

    #                         file = abrirArchivo(FILEPATH)
    #                         # handshakeExitoso = cliente.entablarHandshake(FILENAME, tamanio_archivo, UPLOAD)
    #                         # if (not handshakeExitoso) :
    #                         #       return
    #                         client.enviarArchivo(FILEPATH,backN)
    #                         cerrarArchivo(file)
    #                     if(sys.argv[0] == "download"):
    #                         if(opt in ('-d','--dst')):
    #                             FILEPATH = arg #ruta donde guardo el archivo
    #                             # handshakeExitoso = cliente.entablarHandshake(FILENAME, 0, DOWNLOAD)
    #                             # if (not handshakeExitoso) :
    #                             #      return
                                
    #                              #file = cliente.recibirArchivo(FILEPATH, FILENAME)
    #                             cerrarArchivo(file)

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
    