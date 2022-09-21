from concurrent.futures import ThreadPoolExecutor
from socket import*

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('',serverPort))
print ("The Server is ready receive")

#Tratamos al servidor 

#while True:
#    message, clientAdress = serverSocket.recvfrom(2048)
#    modifiedMessage = message.decode().upper()
#    serverSocket.sendto(modifiedMessage.encode(),clientAdress)


#def connectDistribute():
#La idea atras de este es ser la primer conexion que distribuya los primeros paquetes a los otros puertos



#def recieve():
#La idea atras de esta es ser la que hace la conexion al puerto disponible y asi establecer la conexion y comunicacion
#Osea esta es la funcion que le paso al thread dentro del threadpool para que establezca conexion y se quede en el while recibiendo

#def send():
#La idea atras de esta es ser la que hace la conexion al puerto disponible y asi establecer la conexion y comunicacion
#Osea esta es la funcion que le paso al thread dentro del threadpool para que establezca conexion y se quede en algun loop mandando 
#hasta terminarse el archivo, deberia ser muy parecida a la que usa el cliente PERO es importante que el servidor cambie de puerto


#executor = ThreadPoolExecutor(max_workers= 6)

