from socket import *
import time
import enviador
import paquete

MSJ_SIZE = 5
TAM_VENTANA = 5 #tamanio de la ventana
MAX_WAIT_GOBACKN = 30
MAX_TRIES = 3
MAX_WAIT_ACKS = 5

class GoBackN(enviador.Enviador):

    # GO BACK N TIENE ACK ACUMULATIVOS, SI SE PIERDE UN PAQUETE ME VA A DEVOLVER EL ACK DEL ANTERIOR YA QUE VA A DESCARTAR LOS PAQUETES SIGUIENTES AL QUE PERDIO

    def __init__(self):
        self.older_seq_number = 0
        self.new_seq_number = 0
        self.paquetesEnVuelo = []
        super(GoBackN,self).__init__()

    def enviar(self,mensaje,entidad):
        return 1


    def recibirPaqueteACK(self, entidad) :
        pckRecibido = entidad.recibirPaqueteBackN() #obtengo el ultimo paquete recibido
        ackRecibido = self.gestorPaquetes.actualizarACK(pckRecibido)
        return pckRecibido, ackRecibido


    def enviarPaquete(self,file,entidad):
        #SACAR EL LLAMADO A FUNCION Y EL RETURN
        self.enviarPaqueteFede(file,entidad)
        return
        mensaje = file.read(MSJ_SIZE)
        timeout_start = 0
        while (len(mensaje) > 0):
            
            #si el numero de sequencia del siguiente paquete a enviar es menor al numero de seq del primer paquete que envie
            # -- ENVIAR ACK --
            if(self.new_seq_number < self.older_seq_number + TAM_VENTANA):
                if(self.older_seq_number == self.new_seq_number): #entrás cuando corriste la ventana entera
                    timeout_start = time.time()         
                pck = self.gestorPaquetes.crearPaquete(mensaje)
                self.paquetesEnVuelo.append(pck)
                entidad.enviarPaquete(self.gestorPaquetes.pasarPaqueteABytes(pck))
                self.new_seq_number = pck.obtenerSeqNumber()
            
            
            # -- Espero un poquito de tiempo, porque los paquetes son lentos -- 
            timerEsperaACKs = time.time()
            esACKEsperado= False
            pckRecibido = None
            print("Envie 1")
            while(time.time() < timerEsperaACKs + MAX_WAIT_ACKS) and esACKEsperado == False:
                print("Recibi 1")
                pckRecibido, esACKEsperado = self.recibirPaqueteACK(entidad)
                #agrego esta línea porque antes de continuar intentando enviar, sí o sí me tiene que haber llegado algo
            

            # -- VERIFICACION DE ACK --
            if (esACKEsperado) : #SI RECIBO UN ACK, SIGNIFICA QUE RECIBI EL ACK DEL ULTIMO PAQUETE QUE LLEGO BIEN
                                        # (ES DECIR QUE, TODOS LOS PAQUETES ANTERIORES TMB LLEGARON BIEN)
                #muevo el older_seq_number a la posicion siguiente al new_seq_number
                self.older_seq_number = pckRecibido.obtenerSeqNumber()+1 
                timeout_start = time.time() #reinicio el timer porque los paquetes me llegaron bien, corro el older porque tengo que mandar paquetes nuevos 
                self.paquetesEnVuelo.pop(0) #borro el paquete que llego bien (voy borrando de a uno)
                    

            # -- REENVIAR PCKS EN CASO DE ERROR --
            saltoTimerReenvio = (time.time() - timeout_start)  >= MAX_WAIT_GOBACKN
            if(esACKEsperado == False and  saltoTimerReenvio): #SI SALTO TIMEOUT, ENTONCES PERDI UN PAQUETE Y POR ENDE TENGO 
                                                            #QUE VOLVER A INICIAR EL TIMER Y ENVIAR LOS PAQUETES QUE ME QUEDARON EN LA LISTA DE PAQUETES EN VUELO
                timeout_start = time.time()
                for pck in range(len(self.paquetesEnVuelo)):
                    entidad.enviarPaquete(self.gestorPaquetes.pasarPaqueteABytes(self.paquetesEnVuelo[pck]))
     

            mensaje = file.read(MSJ_SIZE)


    def enviarPaqueteFede(self,file,entidad):
            mensaje = "entrar en ciclo"
            timeout_start = 0
            while (len(mensaje) > 0):
                
                #si el numero de sequencia del siguiente paquete a enviar es menor al numero de seq del primer paquete que envie
                # -- ENVIAR ACK --
                if(self.new_seq_number < self.older_seq_number + TAM_VENTANA):
                    mensaje = file.read(MSJ_SIZE)
                    pck = self.gestorPaquetes.crearPaquete(mensaje)
                    self.paquetesEnVuelo.append(pck)
                    entidad.enviarPaquete(self.gestorPaquetes.pasarPaqueteABytes(pck))
                    self.new_seq_number = pck.obtenerSeqNumber()
                    if(self.older_seq_number == self.new_seq_number): #entrás cuando corriste la ventana entera
                        timeout_start = time.time()    
                    self.new_seq_number += 1  
                    continue
                    
                
                
                """
                # -- Espero un poquito de tiempo, porque los paquetes son lentos -- 
                timerEsperaACKs = time.time()
                esACKEsperado= False
                pckRecibido = None
                print("Envie 1")
                while(time.time() < timerEsperaACKs + MAX_WAIT_ACKS) and esACKEsperado == False:
                    print("Recibi 1")
                    pckRecibido, esACKEsperado = self.recibirPaqueteACK(entidad)
                    #agrego esta línea porque antes de continuar intentando enviar, sí o sí me tiene que haber llegado algo
                """
                #-- IMPLEMENTACION FEDE
                pckRecibido, esACKEsperado = self.recibirPaqueteACK(entidad)
                print(esACKEsperado)
                #if(len(self.paquetesEnVuelo) == TAM_VENTANA and esACKEsperado == False):
                    #continue
                """
                POSIBLE IDEA NO CREO QUE VAYA
                print("Contenido de la ventana es:",len(self.paquetesEnVuelo))
                if(len(self.paquetesEnVuelo) == TAM_VENTANA and esACKEsperado == False):
                    print("Entre al if")
                    while((time.time()-timeout_start) < MAX_WAIT_GOBACKN):
                        #print("recivo acks")
                        pckRecibido, esACKEsperado = self.recibirPaqueteACK(entidad)
                        if(esACKEsperado == True):
                            print("Recibi ack correcto")
                            print("")
                            break
                """

                # -- VERIFICACION DE ACK --
                if (esACKEsperado) : #SI RECIBO UN ACK, SIGNIFICA QUE RECIBI EL ACK DEL ULTIMO PAQUETE QUE LLEGO BIEN
                                            # (ES DECIR QUE, TODOS LOS PAQUETES ANTERIORES TMB LLEGARON BIEN)
                    #muevo el older_seq_number a la posicion siguiente al new_seq_number
                    print("ACK CORRECTO")
                    self.older_seq_number = pckRecibido.obtenerSeqNumber()+1 
                    self.paquetesEnVuelo.pop(0) #borro el paquete que llego bien (voy borrando de a uno)
                    if(self.older_seq_number == self.new_seq_number):
                        #STOP_TIMER QUE SERA ???
                        print("STOP TIMER")
                    else:    
                        timeout_start = time.time() #reinicio el timer porque los paquetes me llegaron bien, corro el older porque tengo que mandar paquetes nuevos 
                    
                        

                # -- REENVIAR PCKS EN CASO DE ERROR --
                var = time.time()
                saltoTimerReenvio = (var - timeout_start)  >= MAX_WAIT_GOBACKN
                #print("TIMEOUT START ES:",timeout_start)
                #print(var - timeout_start)
                if(saltoTimerReenvio and timeout_start != 0): #SI SALTO TIMEOUT, ENTONCES PERDI UN PAQUETE Y POR ENDE TENGO 
                                                                #QUE VOLVER A INICIAR EL TIMER Y ENVIAR LOS PAQUETES QUE ME QUEDARON EN LA LISTA DE PAQUETES EN VUELO
                    print("SALTO EL TIMER")
                    timeout_start = time.time()
                    for pck in range(len(self.paquetesEnVuelo)):
                        entidad.enviarPaquete(self.gestorPaquetes.pasarPaqueteABytes(self.paquetesEnVuelo[pck]))
        


   

"""
El cliente solo va a necesitar un solo timer del paquete en vuelo mas antiguo, cuando se agota el tiempo de espera el cliente
retransmite el paquete N y todos los sucesivos a el. 

Cada vez que recibe un paquete, va a enviar un ACK de los paquetes recibidos correctamente hasta el momento que tiene 
el numero de secuencia mas alto.

"""