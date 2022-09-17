class Paquete:
    windowSize = 0
    sequenceNumber = 0
    acknowledgeNumber = 0
    mensaje = 9 #Desp pensar que deberia ser string o bytes o int

#UDP
#Puerto fuente, Puerto destino, longitud mensaje, checksum, mensaje

#TCP
#Puerto fuente, Puerto destino, longitud mensaje, checksum, mensaje
#Numero de secuencia, Numero de ack, HLEN, Reservado, Indicadores
#Ventana, Puntero de Urgencia, opcional, relleno, datos