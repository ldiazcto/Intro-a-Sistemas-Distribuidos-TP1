from msilib import sequence
from multiprocessing.reduction import ACKNOWLEDGE


CHUNCKSIZE = 32 #en bytes quería poner un a cte, no puedo? =D
SEQUENCE_NUMBER_MAX = 100
WINDOW_SIZE = SEQUENCE_NUMBER_MAX/2

class Paquete:
    sequenceNumber = 0    
    acknowledgeNumber = 0

    def deArchivoABinario(ruta):
        listaPaquetes = []
        sequenceNumber = 0
        with open(ruta,"rb") as file: 
            for chunck in iter(lambda: file.read(CHUNCKSIZE),b''): #leo de a 1 paquete #TE LEE TODO EL ARCHIVO
                sequenceNumber += 1
                acknowledgeNumber += 1
                paquete = (chunck, sequenceNumber, acknowledgeNumber)
                listaPaquetes.append(paquete)
                ##mando por socket
                if(sequenceNumber == WINDOW_SIZE or sequenceNumber == 2*WINDOW_SIZE) :
                    #teneos que esperar a los ack
                    #no es un for, después lo pensamos xd pero es algo para determinar cuántas veces intento reenviar
                    for i in range (0, 3): #intento reenviar el paquete 2 veces. Por hipótesis, si no puedo enviar el window_size entero después de 3 intentos, cierro conexión
                        #si el último ack es menor a WINDOW_SIZe -> perdí paquetes --> los tengo que reenviar, que están en mi lista
                        for paquete in range(len(listaPaquetes)): #revisar, quiero enviar los paquetes de la lista listaPaquetes desde ack+1 a WINDOW_SIZE
                            #reenviar por el socket
                
                    #meto el paquete en una lista
                    #mando el paquete por el socket
                #ya mandé los 50 paquetes, tengo que verificar que los acks que recibo son hasta el que mandé
                
                #si el último ack es menor a WINDOW_SIZE 
                    #--> reenvío los paquetes desde el último que recibí (sin incluir, para no duplicar) hasta WINDOW_SIZE

#Ideas
#Dado que tenemos que determinar diferentes puertos para conectarnos para recibir el stream de bytes en diferentes procesos y asi hacerlo multithread 
#dado que si recibo todo en un solo termina siendo cuello de botella y bloqueante, por ahi hacer un paquete que sea de handshake que espere recibir
#en el ack de ese paquete otro que le indique a que puerto mandar la conexion posta y dejar un puerto para recibir y abrir conexion en esos puertos los cuales
#dejo como disponibles

#UDP
#Puerto fuente, Puerto destino, longitud mensaje, checksum, mensaje

#TCP
#Puerto fuente, Puerto destino, longitud mensaje, checksum, mensaje
#Numero de secuencia, Numero de ack, HLEN, Reservado, Indicadores
#Ventana, Puntero de Urgencia, opcional, relleno, datos