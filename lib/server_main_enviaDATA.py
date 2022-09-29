#main para pruebas de cliente recibiendo paquetes con info

import socket
import gestorPaquetes

FIN = 5
#tiene la info y la envía

def main() :
        receiverName = "localhost"
        receiverPort = 12000
        
        senderSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        mensaje = input("Ingresar mensaje: ")
        gP = gestorPaquetes.Gestor_Paquete()
        pck = gP.crearPaquete(mensaje)
        pckBytes = gP.pasarPaqueteABytes(pck)

        senderSocket.sendto(pckBytes, (receiverName, receiverPort))
        senderSocket.sendto(pckBytes, (receiverName, receiverPort))
        senderSocket.sendto(pckBytes, (receiverName, receiverPort))
        senderSocket.sendto(pckBytes, (receiverName, receiverPort))
        senderSocket.sendto(pckBytes, (receiverName, receiverPort))
        
        pckFin = gP.crearPaqueteFin()
        pckFinBytes = gP.pasarPaqueteABytes(pckFin)
        senderSocket.sendto(pckFinBytes, (receiverName, receiverPort))

        senderSocket.close()

#acá el sender no escucha, sólo envía

main()



""""
| Server |                      | Cliente | 
 Puerto Escucha                   Puerto Escucha
 Puerto Envía                     Puerto Envía
"""