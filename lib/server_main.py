import server_hilo


def main(host, port, filepath, protocolo,logger):
    server_prueba = server_hilo.Server(host,port,filepath,protocolo,logger)

    server_prueba.start()
    while True:
        logger.info("Para detener el servidor ingrese la palabra FIN")
        palabra = input()
        if palabra == "FIN":
            server_prueba.cerrar_socket()
            server_prueba.finalizar()
            logger.info("Se ha finalizado la conexión")
            server_prueba.join()
            return