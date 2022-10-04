from socket import *


class Cliente():
    
        def __init__(self, IP_server, puerto_server, logger):
                self.IP_server = IP_server
                self.puerto_server = puerto_server
                self.logger = logger


        def enviar_archivo(self, sender):
                return sender.enviar_archivo()


        def recibir_archivo(self, receiver):
                return receiver.recibir_archivo()


 