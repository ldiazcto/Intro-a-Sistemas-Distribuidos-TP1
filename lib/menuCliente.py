import sys
import logging
import parser
import sender_stop_wait
import sender
import sender_gobackn
import receiver
import cliente


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
        self.filepath = "" 
        self.port = 8080
        self.serverAdress = "" 
        self.transferencia = ""
        self.cambiar_protocolo = False

    def main(self):

        file_handler = logging.FileHandler(filename='tmp.log')
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
                                        + "-o                 --option protocol in upload")
                                sys.exit(0)
            if sys.argv[1] == "--upload" or sys.argv[1] == "--download":

                self.parser.definirVerbosidad(opt, logger)
                self.port, self.serverAdress = self.parser.definirPuertoYHost(opt, arg, self.port, self.serverAdress)
                if(opt in ('-n','--name')):
                    self.filename = arg
                if(opt in ('-o','--option')):
                    self.cambiar_protocolo = self.parser.cambiarProtocolo()
                if(sys.argv[1] == "--upload"):
                    if(opt in ('-s','--src')):
                        self.filepath = arg
                if(sys.argv[1] == "--download"):
                    if(opt in ('-d','--dst')):
                        self.filepath = arg
            else: 
                logger.error("Debe ingresar una acci??n a realizar [--upload]/[--download]")
                sys.exit(2)
        if(self.filepath == ""):
            logger.error("Debe indicar una ruta de archivo [-s/--src] o [-d/--dst]")
            sys.exit(2)
        if (self.filename == ""):
            logger.error("Debe ingresar el nombre del archivo [-n/--name]")
            sys.exit(2)

        client = cliente.Cliente(self.serverAdress, self.port, logger) 
        if(sys.argv[1] == "--upload"):
            ruta = self.filepath + "/" + self.filename
            protocolo = sender_stop_wait.StopWait(self.serverAdress, int(self.port), self.filename, self.filepath, logger)
            if self.cambiar_protocolo == True : protocolo = sender_gobackn.GoBackN(self.serverAdress, int(self.port), self.filename, self.filepath,logger)
            client.enviar_archivo(protocolo)
        else:
            rec = receiver.Receiver(self.serverAdress, int(self.port), self.filepath,self.filename, logger)
            client.recibir_archivo(rec)

        return 0

if __name__ == "__main__":
    menuCliente = MenuCliente()
    menuCliente.main()    
