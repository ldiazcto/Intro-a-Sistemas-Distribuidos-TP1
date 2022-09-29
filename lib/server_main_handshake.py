import gestorPaquetes
import server_hilo
UPLOAD = 2
ACK_CORRECT = 1
def cerrarArchivo(file):
    if (file is not None) :
        file.close()

#envía el handshake

def meVoy(serverPrueba):
        serverPrueba.cerrar_socket()
        serverPrueba.finalizar()
        serverPrueba.join()

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

        #server recibe handshake
        paquete = serverPrueba.recibirHandshake()
        if (paquete == None) :
                print("Nunca me llegó nada del cliente, me voy")
                meVoy(serverPrueba)
                return

        handshakeApropiado = serverPrueba.chequearHandshakeApropiado(paquete)
        if (not handshakeApropiado) :
                print("Se envió un paquete que no es handshake, me voy")
                meVoy(serverPrueba)
                return

        #server chequea tamaño
        tamanioApropiado = serverPrueba.chequearTamanio(paquete)
        if (not tamanioApropiado) :
                print("El tamaño pasado no es apropiado, me voy")
                print("Debería mandar un ack de que está mal lo que me pasaron? qué número de ack tendría?")
                meVoy(serverPrueba)
                return
        
        archivoExiste = serverPrueba.chequearExistenciaArchivo(paquete)
        if (not archivoExiste) :
                print("El archivo pedido no existe, me voy")
                meVoy(serverPrueba)
                return

        #server envia paquete ack
        serverPrueba.enviarACKHandshake()

        if serverPrueba.esHandshakeUpload(paquete) :
                x=1
                #lógica para el upload
        else :
                x=2
                #lógica para el download
        
        #fin
        meVoy(serverPrueba)
        



def iniciaHandshakeDOWNLOAD():
        print("Aun no implementado :)")


print("--PRUEBA CLIENTE INICIA HANDSHAKE UPLOAD--")
iniciaHandshakeUPLOAD()

print("--PRUEBA CLIENTE RECIBE HANDSHAKE DOWNLOAD--")
iniciaHandshakeDOWNLOAD()
