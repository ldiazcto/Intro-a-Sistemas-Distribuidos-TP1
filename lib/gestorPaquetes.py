import paquete

DATA = 0 #a veces llamado NOT_ACK
ACK = 1
UPLOAD = 2
DOWNLOAD = 3
REFUSED = 4
FIN = 5

class Gestor_Paquete:
    def __init__(self):
        self.seq_number = 1
        self.ack_number_receiver = 0
        self.ack_number_sender = 1
        self.seq_number_receiver = 1
        self.COMIENZA_DATA = 4
        self.COMIENZA_SEQ_NUMBER = 0
        self.FIN_SEQ_NUMBER = 2
        self.COMIENZA_ACK = 2
        self.FIN_ACK = 4
    
    def crearPaquete(self, mensaje):
        pck = paquete.Paquete(self.seq_number, DATA, mensaje)
        self.seq_number += 1
        return pck

    def crearPaqueteACK(self, agregado):
        self.seq_number += agregado 
        self.ack_number_receiver += agregado
        return paquete.Paquete(self.ack_number_receiver, ACK, None)

    def crearPaqueteHandshake(self, operador, mensaje):
        return paquete.Paquete(self.seq_number, operador, mensaje)

    def crearPaqueteRefused(self):
        return paquete.Paquete(self.seq_number, REFUSED, None)    
        
    def crearPaqueteFin(self):
        return paquete.Paquete(self.seq_number, FIN, None)    

    def pasarBytesAPaquete(self, paqueteBytes):
        seq_number_recibido = int.from_bytes(paqueteBytes[self.COMIENZA_SEQ_NUMBER:self.FIN_SEQ_NUMBER],"big")
        ack_recibido = int.from_bytes(paqueteBytes[self.COMIENZA_ACK:self.FIN_ACK],"big")
        mensaje = paqueteBytes[self.FIN_ACK:]

        return paquete.Paquete(seq_number_recibido, ack_recibido, mensaje)

    def pasarPaqueteABytes(self, pck):
        sequence = pck.obtenerSeqNumber().to_bytes(2,byteorder="big")
        ack = (pck.obtenerOperador()).to_bytes(2,byteorder="big") 
        mensaje = pck.obtenerMensaje()
        paqueteBytes = sequence
        paqueteBytes += ack
        if (mensaje != None):
            if pck.esUpload() or pck.esDownload():
                mensaje =  bytes(mensaje, 'utf-8')
            paqueteBytes += mensaje
        return paqueteBytes
    
    
    def cierreConexion(self,FIN):
        pck = paquete.Paquete(self.seq_number,FIN,None)
        return pck.esFin()
    
    def verificarACK(self,pck):
        if (pck == None):
            return False
        if (pck.esACK() == True): 
            if(pck.obtenerSeqNumber() >= self.ack_number_sender):
                self.ack_number_sender = pck.obtenerSeqNumber()
                return True 
        return False

    def actualizarACK(self, pck):
        verificacion = self.verificarACK(pck)
        if(verificacion == True):
            self.ack_number_sender += 1
        return verificacion
        
    def verificarRefused(self, pck):
        if pck == None:
            return False
        return pck.esRefused()

    def verificarPaqueteOrdenado(self,paquete):
        if (paquete == None):
            return False
        return (paquete.obtenerSeqNumber() == self.seq_number)
    