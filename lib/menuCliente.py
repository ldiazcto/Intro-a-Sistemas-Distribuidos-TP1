import os
import cliente, stopAndWait, goBackN #nombre del archivo
import getopt
import sys
import logging
import parser

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

class MenuCliente:

    def __init__(self):    
        self.parser = parser.Parser()
        self.filename = ""
        self.filepath = "" # -s para upload -d para download
        self.port = 8080
        self.serverAdress = "" # --host/ -H
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
                                print("usage : upload [-h] [-v | -q] [-H ADDR ] [-p PORT ] [-s FILEPATH ] [-n FILENAME ]\n" 
                                            + "<command description >\n "
                                        + " optional arguments : "
                                        + "-h,                --help show this help message and exit\n " 
                                        + "-v,                -- verbose increase output verbosity\n "
                                        + "-q,                --quiet decrease output verbosity\n "
                                        + "-H,                --host server IP address\n "
                                        + "-p,                --port server port\n "
                                        + "-s,                --src source file path\n "
                                        + "-n,                --name file name\n"
                                        + "-o                 --option protocol")
                                sys.exit(0)
            if sys.argv[1] == "--upload" or sys.argv[1] == "--download":
                print("Entro a elegir mis opciones: ", opt)

                self.parser.definirVerbosidad(opt, logger)
                self.port, self.serverAdress = self.parser.definirPuertoYHost(opt, arg, self.port, self.serverAdress)
                
                if(opt in ('-n','--name')):
                    self.filename = arg
                
                if(opt in ('-o','--option')):
                    self.protocolo = self.parser.cambiarProtocolo()
                    
                # ---------------------------------UPLOAD
                if(sys.argv[1] == "--upload"):
                    if(opt in ('-s','--src')):
                        self.filepath = arg
                        self.transferencia = UPLOAD

                #---------------------------------DOWNLOAD
                if(sys.argv[1] == "--download"):
                    if(opt in ('-d','--dst')):
                        self.filepath = arg
                        self.transferencia = DOWNLOAD   
            else: 
                logger.error("Debe ingresar una acción a realizar [--upload]/[--download]")
                sys.exit(2)

        #Si termine de recorrer mis argumentos y nunca tuve el path para el up o download
        if(self.filepath == ""):
            logger.error("Debe indicar una ruta de archivo [-s/--src] o [-d/--dst]")
            sys.exit(2)
        if (self.filename == ""):
            logger.error("Debe ingresar el nombre del archivo [-n/--name]")
            sys.exit(2)


        #Ya parsie, setie, se la transferencia, ahora procedo a intentar hacerla, handhshake
        sender = sender
        cliente = cliente.Cliente("localhost", self.port, 12000) #server adress Ip adress,  puertoEntradaContrario
        if(sys.argv[1] == "--upload"):
            ruta = self.filepath + "/" + self.filename
            print("Mi file es: ", ruta)
            file = self.abrirArchivo(ruta)
            filesize = os.path.getsize(ruta)
            #handshakeExitoso = cliente.entablarHandshake(self.filename, filesize, UPLOAD)
            handshakeExitoso = sender.entablarHandshake(self.filename, filesize, UPLOAD)
            if handshakeExitoso == True:
                logger.info("El handshake resulto exitoso")
                logger.info("Se envia el archivo...")
                cliente.enviarArchivo(file,self.protocolo)
            else:
                logger.debug("El handshake fallo")
            self.cerrarArchivo(file)
        else:
            #Para el download
            handshakeExitoso = cliente.entablarHandshake(ruta, tamanio_archivo, DOWNLOAD)
            if handshakeExitoso == True : 
                logger.info("El handshake resulto exitoso")
                logger.info("Se envia el archivo...")
                cliente.recibirArchivo(self.filepath,self.filename, self.protocolo)
            else:
                logger.debug("El handshake fallo")

        return 0

if __name__ == "__main__":
    menuCliente = MenuCliente()
    menuCliente.main()

    
