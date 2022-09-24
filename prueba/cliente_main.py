import cliente
import getopt
import sys

def main():

    cliente_prueba = cliente()
    while True:
        print ("Escriba mensaje")
        mensaje = input()
        cliente_prueba.mandarPaquete(mensaje)

"""
    ADDR = ""
    PORT = 0
    FILEPATH = ""
    FILENAME = ""

    opcionesCortas = "hvqH:p:s:n:d:" #se utilizan con -. DUDA: a los que le precede : van con un argumento extra, por ej >>python upload -H ADDR , esta bien eso??
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
                    ADDR = arg
                    #direccion IP del servidos
                if(opt in ('-p','--port')):
                    PORT = arg
                    #puerto del servidor
                if(opt in ('-n','--name')):
                    FILENAME = arg
                    #nombre del paquete   
                if(sys.argv[0] == "upload"):
                    if(opt in ('-s','--src')):
                            FILEPATH = arg
                            #ruta de origen del paquete
                if(sys.argv[0] == "download"):
                    if(opt in ('-d','-dst')):
                        FILEPATH = arg
                        #ruta de destino del paquete
                sys.exit(0)
        except sys.argv[0] != "upload" and sys.argv[0] != "download":
            print(" -- DEAD CONNECTION --")
            sys.exit(2)

    return 0
    """

#main()