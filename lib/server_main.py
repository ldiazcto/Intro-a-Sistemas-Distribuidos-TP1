import server_hilo


def main():
    # server_prueba = server_hilo.Server("localhost",9000,"/home/fede/Desktop/distribuidos/alternativa_2/Intro-a-Sistemas-Distribuidos-TP1/lib/BDD_Servidor","GN")
    server_prueba = server_hilo.Server("localhost",9000,"/Users/luzmi/OneDrive/2FIUBA/75.43-INTRO-A-DISTRIBUIDOS/¨TP1-Intro/lib/BDD_Cliente/BDD_Servidor","GN")

    server_prueba.start()
    while True:
        print ("Para detener el servidor ingrese la palabra FIN")
        palabra = input()
        if palabra == "FIN":
            server_prueba.cerrar_socket()
            server_prueba.finalizar()
            server_prueba.join()
            print ("LLEGO HASTA ACA")
            return

main()
print ("LLEGO HASTA ACA")
