import cliente, stopAndWait, goBackN #nombre del archivo
import getopt
import sys

SERVER_ADDR = ""
SERVER_PORT = 120
FILEPATH = ""
FILENAME = ""

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
                    
#     if (opt in ('-q','--quiet')):
#         verbosity -= 1
    


# def definirPuertoYNombre(opt, arg):
#     if(opt in ('-p','--port')):
#         SERVER_PORT = arg
#         #puerto del servidor
                    
#     if(opt in ('-n','--name')):
#         FILENAME = arg
#         #nombre del paquete


def main():
   
    cliente_prueba = cliente.Cliente("localhost", 120)
    stopWait = stopAndWait.StopAndWait()
    #backN = goBackN.GoBackN() #llamo a la clase, y me ejecuta el constructor
    print("Se creo el cliente con exito")
    cliente_prueba.enviarArchivo("./lib/hola.txt",stopWait)
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
    #                         if(opt in ('-s','--src')):
    #                             FILEPATH = arg
    #                             #ruta de origen del paquete
    #                             client.enviarArchivo(FILEPATH,backN)
    #                     if(sys.argv[0] == "download"):
    #                         if(opt in ('-d','--dst')):
    #                             print("No está implementado")
    #                             FILEPATH = arg
    #                             #ruta de destino del paquete
    #                             #cliente.recibirArchivo(FILEPATH)
    #                 cambiarModo = input("Quiere cambiar de protocolo? S/N: \n")
    #                 if(cambiarModo == "N"):
    #                     seguir = False
    #                 elif(cambiarModo == "S"):
    #                     protocolo = input("Elegir protocolo (S/G): \n")
    #                     seguir = True
    #                 else:
    #                     return
    #         sys.exit(0)

    #     except sys.argv[0] != "upload" and sys.argv[0] != "download":
    #         print(" -- DEAD CONNECTION --")
    #         sys.exit(2)

main()