import gestorPaquetes
import server_hilo
UPLOAD = 2
ACK_CORRECT = 1
def cerrarArchivo(file):
    if (file is not None) :
        file.close()

#envía el handshake


def iniciaHandshakeUPLOAD():
   
        #soy server
        #recibo paquete
        #lo parseo y chequeo tamaño
        #si tamaño correcto, mando ack de handshake

        #server iniciado
        receiverName = "localhost"
        receiverPort = 12000
        
        serverPrueba = server_hilo.Server()
        serverPrueba.start()
        print("\nServer: volví de start")

        while True:
                print ("Para detener el servidor ingrese la palabra FIN")
                palabra = input()
                if palabra == "FIN":
                        serverPrueba.cerrar_socket()
                        serverPrueba.finalizar()
                        serverPrueba.join()
                        print ("LLEGO HASTA ACA")
                        break
                
        #fin
        print("Termino todo bien, me voy :D")
        



def iniciaHandshakeDOWNLOAD():
        print("Aun no implementado :)")


print("\n\n--PRUEBA SERVER INICIA HANDSHAKE UPLOAD--")
iniciaHandshakeUPLOAD()

print("\n\n--PRUEBA SERVER RECIBE HANDSHAKE DOWNLOAD--")
iniciaHandshakeDOWNLOAD()
