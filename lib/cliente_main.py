import cliente, stopAndWait, goBackN #nombre del archivo
import getopt
import sys

def main():

    cliente_prueba = cliente.Cliente("localhost", 120)
    #stopWait = stopAndWait.StopAndWait()
    backN = goBackN.GoBackN() #llamo a la clase, y me ejecuta el constructor
    print("Se creo el cliente con exito")
    cliente_prueba.subirArchivo("./lib/hola.txt",backN)
    return 0
"""
    SERVER_ADDR = ""
    SERVER_PORT = 12000
    FILEPATH = ""
    FILENAME = ""

    opcionesCortas = "hvqH:p:s:n:d:" #se utilizan con -. 
    opcionesLargas = ["help","verbose","quiet","host=","port=","src=","name=","dst="] #se utilizan con --

    listaArgumentos = sys.argv[1:]
    try:
        opciones, argumentos = getopt.getopt(listaArgumentos,opcionesCortas,opcionesLargas) #par tuplas
    except getopt.error as err:
        print(str(err))
        sys.exit(2)   #conexion muerta


    for opt,arg in opciones: #para entrar en las tuplas de opciones y analizar
        try:
            if(sys.argv[0] == "upload" or sys.argv[0] == "download"):
                if(opt in ('-h,'--help')):
                    #mostrar mensaje de ayuda
                    sys.exit(0) #salir con exito
                if(opt in ('-v','--verbose')):
                    #aumentar la verbosidad de salida
                if(opt in ('-q','--quiet')):
                    #decrementar la verbosidad de salida
                if(opt in ('-H','--host)):
                    SERVER_ADDR = arg
                    #direccion IP del servidor
                if(opt in ('-p','--port')):
                    SERVER_PORT = arg
                    #puerto del servidor
                if(opt in ('-n','--name')):
                    FILENAME = arg
                    #nombre del paquete

                #cliente se inicializa
                client = cliente(SERVER_ADDR, SERVER_PORT)
                if(sys.argv[0] == "upload"):
                    if(opt in ('-s','--src')):
                        FILEPATH = arg
                        #ruta de origen del paquete
                        #cliente.subirArchivo(FILEPATH)
                if(sys.argv[0] == "download"):
                    if(opt in ('-d','-dst')):
                        FILEPATH = arg
                        #ruta de destino del paquete
                        #cliente.descargarArchivo(FILEPATH)
                sys.exit(0)
        except sys.argv[0] != "upload" and sys.argv[0] != "download":
            print(" -- DEAD CONNECTION --")
            sys.exit(2)
    """
    


main()