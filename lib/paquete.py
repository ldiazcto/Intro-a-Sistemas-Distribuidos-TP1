#from asyncio.windows_events import NULL
from time import time as timer

NOT_ACK = -1

class Paquete:
    def __init__(self,sequenceNumber,ackNumber, mensaje):
        self.sequenceNumber = sequenceNumber
        self.ackNumber = ackNumber
        self.mensaje = mensaje

    def esACK(self):
        return (self.ackNumber != NOT_ACK)
        
    def obtenerACK(self):
        if (self.esACK()):
            return self.ackNumber
        return 0



    #3 bytes para sequebce
    #3 bytes para ackNUmber
    #5 bytes para mensaje
    def pckEncode(self,mensaje):
        sequence = (self.sequenceNUmber).to_bytes(3,byteorder="big")
        ack = (self.ackNumber).to_bytes(3,byteorder="big")
        
        encoded += sequence
        encoded += ack
        encoded += mensaje

        return encoded



    #no te entendi fede a que te referis? onda la idea es para el decode que arme un paquete otra vez no?
    #A okok te entiendo eso deberia andar aunque no es el problema onda lo mio es con decode


    #en vez de paquete se podria llamar Fabrica_paquete
    #en encode le pasas el mensaje y te devuelve el mensaje ya encodeado
    #Fabrica_paquete.encode(data)

    #en decode nos guardamos las posiciones de los ack y seq_number como atributos
    #y sacamos la data y la devolvemos
    def pckDecode(tiraBytes): 
        decodificado = paquete(int.from_bytes(tiraBytes[0:2],"big"), int.from_bytes(tiraBytes[2:4],"big"), tiraBytes[4:])
        return decodificado
