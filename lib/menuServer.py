import os
import cliente, stopAndWait, goBackN
import getopt
import sys
import logging
import parser
import server_main

SERVER_ADDR = ""
SERVER_PORT = 12000
FILEPATH = ""
FILENAME = ""
UPLOAD = 2
DOWNLOAD = 3
PROTOCOLO = stopAndWait.StopAndWait() #Si no me ingresa un protocolo por default elijo este

#NIVELES DE LOGS
NOTSET = 0
DEBUG = 10
INFO = 20
WARNING = 30
CRITICAL = 50
QUIET = 51

class MenuServer:

    def __init__(self):    
        self.parser = parser.Parser()
        self.filepath = "" # storage dir path
        self.port = 12000   # --->service port
        self.host = "" # --host ->service IP address
        self.transferencia = ""
        self.protocolo = stopAndWait.StopAndWait()

    def abrirArchivo(self, ruta):
        try:
            file = open(ruta,'rb')
            return file
        except FileNotFoundError: #o IOERROR o FileExistsError
            print("FILE NO ENCONTRADO")
            sys.exit(2)

    def cerrarArchivo(self, file):
        file.close()

    def main(self):

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
        
        opciones, argumentos = self.parser.obtenerArgumentos()
        print("OPCIONES: ",opciones , argumentos)

        for opt,arg in opciones: #para entrar en las tuplas de opciones y analizar
            if (opt in ('-h','--help')):
                                print("usage : start - server [-h] [-v | -q] [-H ADDR ] [-p PORT ] [-s DIRPATH ]\n" 
                                            + "<command description >\n "
                                        + " optional arguments : "
                                        + "-h, --help                 show this help message and exit\n " 
                                        + "-v, -- verbose             increase output verbosity\n "
                                        + "-q, --quiet                decrease output verbosity\n "
                                        + "-H, --host                 server IP address\n "
                                        + "-p, --port                 server port\n "
                                        + "-s, --storage              storage dir path\n"
                                        + "-o  --option               protocol")
                                sys.exit(0)
            if sys.argv[1] == "--start-server":
                print("Entro a elegir mis opciones: ", opt)

                self.parser.definirVerbosidad(opt, logger)
                self.port, self.serverAdress = self.parser.definirPuertoYHost(opt, arg, self.port, self.serverAdress)

                if(opt in ('-o','--option')):
                    self.protocolo = self.parser.cambiarProtocolo()

                if(opt in ('-s','--storage')):
                    self.filepath = arg
            else: 
                logger.error("Debe iniciar el server [--start-server]")
                sys.exit(2)

        #Si termine de recorrer mis argumentos y nunca ingreso el path donde almacena los archivos 
        if(self.filepath == ""):
            logger.error("Debe indicar una ruta de archivo [-s/--storage]")
            sys.exit(2)

        #Si llegue aca, entonces puedo levantar el server 
        #
        #
        #
        # Le tengo que pasar por parametro la info que me pasaron por comando
        # el host (Service IP adress), Service port, filepath, y protocolo
        server_main.main()
        return 0

if __name__ == "__main__":
    menuServer = MenuServer()
    menuServer.main()

    