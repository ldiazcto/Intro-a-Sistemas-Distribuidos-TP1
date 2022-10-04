import server_hilo


def main(host, port, filepath, protocolo,logger):
    # server_prueba = server_hilo.Server("localhost",9000,"/home/fede/Desktop/distribuidos/alternativa_2/Intro-a-Sistemas-Distribuidos-TP1/lib/BDD_Servidor","GN")
    # server_prueba = server_hilo.Server("localhost",9000,"/Users/luzmi/OneDrive/2FIUBA/75.43-INTRO-A-DISTRIBUIDOS/¨TP1-Intro/lib/BDD_Servidor","GN")
    server_prueba = server_hilo.Server(host,port,filepath,protocolo,logger)

    server_prueba.start()
    while True:
        print ("Para detener el servidor ingrese la palabra FIN")
        palabra = input()
        if palabra == "FIN":
            server_prueba.cerrar_socket()
            server_prueba.finalizar()
            logger.info("Se ha finalizado la conexión")
            server_prueba.join()
            print ("LLEGO HASTA ACA")
            return

# main(host, port, filepath, protocolo)
print ("LLEGO HASTA ACA")
