import sys
import logging
import parser
import server_main


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
        self.filepath = ""
        self.port = 12000
        self.host = "" 
        self.transferencia = ""
        self.protocolo = "sw"

    def main(self):

        file_handler = logging.FileHandler(filename='server.log')
        stdout_handler = logging.StreamHandler(stream=sys.stdout)
        handlers = [file_handler, stdout_handler]
        logging.basicConfig(
            level=logging.INFO, 
            format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
            handlers=handlers
        )
        logger = logging.getLogger()
        opciones, argumentos = self.parser.obtenerArgumentos()
        for opt,arg in opciones: 
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
                self.parser.definirVerbosidad(opt, logger)
                self.port, self.host = self.parser.definirPuertoYHost(opt, arg, self.port, self.host)
                if(opt in ('-o','--option')):
                    self.protocolo = "GN"
                if(opt in ('-s','--storage')):
                    self.filepath = arg
            else: 
                logger.error("Debe iniciar el server [--start-server]")
                sys.exit(2)
        if(self.filepath == ""):
            logger.error("Debe indicar una ruta de archivo [-s/--storage]")
            sys.exit(2)
        server_main.main(self.host,int(self.port),self.filepath,self.protocolo,logger)
        return 0

if __name__ == "__main__":
    menuServer = MenuServer()
    menuServer.main()

    