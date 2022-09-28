import paquete

DATA = 0 #a veces llamado NOT_ACK
ACK = 1
UPLOAD = 2
DOWNLOAD = 3
REFUSED = 4

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
    
    #cuando leo el mensaje desde el archivo
    def crearPaquete(self, mensaje):
        pck = paquete.Paquete(self.seq_number, DATA, mensaje)
        self.seq_number += 1
        return pck
    
    #cuando creas un paquete de tipo ACK
    def crearPaqueteACK(self, agregado):
        self.seq_number_receiver += agregado
        self.ack_number_receiver += agregado
        return paquete.Paquete(self.ack_number_receiver, ACK, None)

    def cierreConexion(self,FIN):
        pck = paquete.Paquete(self.seq_number,FIN,None)
        return pck.esFin()
    
    def crearPaqueteHandshake(self, operador, mensaje):
        return paquete.Paquete(self.seq_number, operador, mensaje)

    def crearPaqueteRefused(self):
        return paquete.Paquete(self.seq_number, REFUSED, None)    

    #cuando lo recibo del socket
    def pasarBytesAPaquete(self, paqueteBytes):
        seq_number_recibido = int.from_bytes(paqueteBytes[self.COMIENZA_SEQ_NUMBER:self.FIN_SEQ_NUMBER],"big")
        ack_recibido = int.from_bytes(paqueteBytes[self.COMIENZA_ACK:self.FIN_ACK],"big")
        mensaje = paqueteBytes[self.FIN_ACK:]

        return paquete.Paquete(seq_number_recibido, ack_recibido, mensaje)

    #cuando lo envío al socket
    def pasarPaqueteABytes(self, pck):
        sequence = pck.obtenerSeqNumber().to_bytes(2,byteorder="big")
        ack = (pck.obtenerOperador()).to_bytes(2,byteorder="big") #Aca deberia llamar a la función o es lo que paquete tiene seteado (?)
        #mensaje = bytes(pck.obtenerMensaje(), 'utf-8')#FIJARSE ACA, pq para convertir str a bytes en python es con otra func
        mensaje = pck.obtenerMensaje()
        #print("El mensaje es ", mensaje)

        paqueteBytes = sequence
        paqueteBytes += ack
        if (mensaje != None):
            paqueteBytes += pck.obtenerMensaje()

        print("paqueteBytes: ", paqueteBytes)
        return paqueteBytes

    def verificarACK(self,pck):
        if(pck.esACK() == True): #es ack entonces me fijo si coincide el numero de ack con el global para saber si llego todo ok
            if(pck.obtenerSeqNumber() == self.ack_number_sender):
                self.ack_number_sender += 1
                return True #llego bien el paquete
        return False


    def verificar_mensaje_recibido(self,paquete):
        return (paquete.obtenerSeqNumber() == self.seq_number_receiver)
        

    """
    def obtener_data(self,mensaje):
        return mensaje[self.COMIENZA_DATA:]

    def verificar_mensaje(self,mensaje):
        seq_number_recibido = int.from_bytes(mensaje[self.COMIENZA_SEQ_NUMBER:self.FIN_SEQ_NUMBER],"big")
        if(seq_number_recibido == self.seq_number):
            self.seq_number += 1
            return True
    
    def verificar_ack(self,mensaje):
        seq_number_recibido = int.from_bytes(mensaje[self.COMIENZA_SEQ_NUMBER:self.FIN_SEQ_NUMBER],"big")
        ack_recibido = int.from_bytes(mensaje[self.COMIENZA_ACK:self.FIN_ACK],"big")
        if(seq_number_recibido == self.seq_number and ack_recibido == 1):
            self.seq_number += 1
            return True
    
    def verificar_paquete_ack(self,paquete):
        seqNumberObtenido = paquete.obtenerSeqNumber()
        return (seqNumberObtenido == self.seq_number - 1)

    """

"""
---Para enviar mensaje---
leer_archivo -> mensaje_bytes
gestor -> crea_paquete
gestor-> devolver_tira_bytes
enviar -> tira_bytes
recibir->ack (continuar de acuerdo a esto)

leo del archivo -> mensaje_bytes -> paquete -> paqueteBytes -> lo envío
                
leo del archivo -> mensaje_bytes -> gestor.crear_paquete(mensaje_bytes) -> gestor.obtener_tira_bytes(paquete) -> enviar_paquete(tira_bytes)



---Recibir mensaje---
recibir->tira_bytes (con recevfrom o lo que sea, del socket)
(Listo) - gestor-> pasar_bytes_a_paquete (creamos entidad paquete y laburamos con el paquete)
gestor-> verificar_paquete (si el paquete esperao era el correcto o se perdió uno en el camino)
    si llego bien el paquete -> escribir_el_archivo -> mensaje
gestor -> crear_ack (ya sea positivo o negativo)
enviar-> ack (por socket)

"""
"""
CODIGO:
0 DATA
1 ES ACK
2 Upload
    mensaje = filename-tamaño
3 DOWNLOAD
    mensaje = filename
"""