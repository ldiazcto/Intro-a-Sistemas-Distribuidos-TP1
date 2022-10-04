from socket import *


class Cliente():
    
        def __init__(self, IP_server, puerto_server, logger):
                self.IP_server = IP_server
                self.puerto_server = puerto_server
                self.logger = logger


        def enviar_archivo(self, sender):
                self.logger.info("Se intenta enviar el archivo...")
                sender.enviar_archivo(self.logger)


        def recibir_archivo(self, receiver):
                receiver.recibir_archivo()


 