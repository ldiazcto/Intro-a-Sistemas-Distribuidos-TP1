from fileinput import filename
import goBackN
import stopAndWait
import sys
import getopt
import logging
import menuCliente
import sender_gobackn

# SERVER_ADDR = ""
# SERVER_PORT = 12000
# FILEPATH = ""
# FILENAME = ""
# UPLOAD = 2
# DOWNLOAD = 3
# PROTOCOLO = stopAndWait.StopAndWait() #Si no me ingresa un protocolo por default elijo este

#NIVELES DE LOGS
NOTSET = 0
DEBUG = 10
INFO = 20
WARNING = 30
CRITICAL = 50
QUIET = 51

class Parser:
    def abrirArchivo(self,ruta):
        try:
            file = open(ruta,'rb')
            return file
        except FileNotFoundError: #o IOERROR o FileExistsError
            print("FILE NO ENCONTRADO")
            sys.exit(2)

    def cerrarArchivo(self,file):
        file.close()

    def obtenerArgumentos(self):
        opcionesCortas = "uhvqH:p:s:d:n:o:" #se utilizan con -. los : esperan su sgte entrada
        opcionesLargas = [ "download","upload", "start-server", "help","verbose","quiet","host=","port=","src=","name=","dst=", "option="] #se utilizan con --
        listaArgumentos = sys.argv[1:]
        try:
            return getopt.getopt(listaArgumentos,opcionesCortas,opcionesLargas) #par tuplas
        except getopt.error as err:
            print(str(err))
            sys.exit(2)   #conexion muerta

    def definirVerbosidad(self, opt, logger):
        if ((opt in ('-v','--verbose')) and opt in (('-q','--quiet'))):
            print("Se pide alta y baja verbosidad a la vez. Por favor, elegir uno o ninguno.")
            sys.exit(0)

        if(opt in ('-v','--verbose')):
            logger.setLevel(DEBUG)         
                        
        if (opt in ('-q','--quiet')):
            logger.setLevel(QUIET)

    def definirPuertoYHost(self, opt, arg, port, host):
        if(opt in ('-p','--port')):
            port = arg #puerto del servidor
            
        if(opt in ('-H','--host')):
            host = arg #nombre del paquete
            
        return port, host

    def cambiarProtocolo(self):
           return True           
