import server_hilo


def main():
    server_prueba = server_hilo.Server()
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