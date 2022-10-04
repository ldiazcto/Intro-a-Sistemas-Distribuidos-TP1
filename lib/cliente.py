from socket import *


class Cliente():
    
        def __init__(self, IP_server, puerto_server, logger):
                self.IP_server = IP_server
                self.puerto_server = puerto_server
                self.logger = logger

        def enviar_archivo(self, sender):
                self.logger.info("Se intenta hacer upload...")
                sender.enviar_archivo(self.logger)
                self.logger.info("✓ Se realizó el upload con éxito")


        def recibir_archivo(self, receiver):
                self.logger.info("Se intenta hacer download...")
                receiver.recibir_archivo()
                self.logger.info("✓ Se realizó el download con éxito")


 