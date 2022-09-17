from socket import *
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = input("Input Lower case sentence:")
clientSocket.sendto(message.encode(),(serverName,serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
clientSocket.close()

def cargarArchivos(ruta):
    listaLineas = []
    with open(ruta,"r") as file:
        for linea in file:
            linea = linea.rstrip("\n").split(",")
            listaLineas.append(linea)
    for linea in listaLineas:
        clientSocket.sendto(linea.encode(),(serverName,serverPort))
        modifiedMessage, serverAddress, ack = clientSocket.recvfrom(2048)
        
        