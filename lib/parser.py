from fileinput import filename
import sys
import getopt
import logging
import menuCliente
import sender_gobackn


#NIVELES DE LOGS
NOTSET = 0
DEBUG = 10
INFO = 20
WARNING = 30
CRITICAL = 50
QUIET = 51

class Parser:

    def obtenerArgumentos(self):
        opcionesCortas = "uhvqH:p:s:d:n:o:" 
        opcionesLargas = [ "download","upload", "start-server", "help","verbose","quiet","host=","port=","src=","name=","dst=", "option="] 
        listaArgumentos = sys.argv[1:]
        try:
            return getopt.getopt(listaArgumentos,opcionesCortas,opcionesLargas)
        except getopt.error as err:
            print(str(err))
            sys.exit(2)   

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
            port = arg 
            
        if(opt in ('-H','--host')):
            host = arg 
            
        return port, host

    def cambiarProtocolo(self):
           return True           
