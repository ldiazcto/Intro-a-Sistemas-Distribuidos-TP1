


class Gestor_Paquete():
    def __init__(self):
        self.seq_number = 1
        self.ack = 1
        self.COMIENZA_DATA = 4
        self.COMIENZA_SEQ_NUMBER = 0
        self.FIN_SEQ_NUMBER = 2
        self.COMIENZA_ACK = 2
        self.FIN_ACK = 4
    
    def obtener_data(self,mensaje):
        return mensaje[self.COMIENZA_DATA:]
    
    def verificar_mensaje(self,mensaje):
        seq_number_recibido = int.from_bytes(mensaje[self.COMIENZA_SEQ_NUMBER:self.FIN_SEQ_NUMBER],"big")
        if(seq_number_recibido == self.seq_number):
            self.seq_number += 1
            return True
    
    def obtener_seq_number(self):
        return self.seq_number - 1
    
    def realizar_paquete_ack(self,seq_number):
        sequence = (seq_number).to_bytes(2,byteorder="big")
        ack = (self.ack).to_bytes(2,byteorder="big")

        paquete  = sequence
        paquete += ack

        return paquete
    
