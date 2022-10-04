from socket import *
import time
import paquete

MSJ_SIZE = 1500
TAM_VENTANA = 50 #tamanio de la ventana
MAX_WAIT_GOBACKN = 5
MAX_TRIES = 3
MAX_WAIT_ACKS = 5
MAX_WAIT_FIN = 10

class GoBackN():

    # GO BACK N TIENE ACK ACUMULATIVOS, SI SE PIERDE UN PAQUETE ME VA A DEVOLVER EL ACK DEL ANTERIOR YA QUE VA A DESCARTAR LOS PAQUETES SIGUIENTES AL QUE PERDIO

    def __init__(self):
        self.older_seq_number = 1
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
            while (True):
                
                #si el numero de sequencia del siguiente paquete a enviar es menor al numero de seq del primer paquete que envie
                # -- ENVIAR ACK --
                if(self.new_seq_number < self.older_seq_number + TAM_VENTANA):
                    mensaje = file.read(MSJ_SIZE)
                    if(len(mensaje) != 0):
                        pck = self.gestorPaquetes.crearPaquete(mensaje)
                        self.paquetesEnVuelo.append(pck)
                        entidad.enviarPaquete(self.gestorPaquetes.pasarPaqueteABytes(pck))
                        #print ("Envio Mensaje: ",self.gestorPaquetes.pasarPaqueteABytes(pck))
                        self.new_seq_number = pck.obtenerSeqNumber()
                        if(self.older_seq_number == self.new_seq_number): #entrás cuando corriste la ventana entera
                            timeout_start = time.time()    
                        #self.new_seq_number += 1  
                        continue
                    
                if(len(self.paquetesEnVuelo) == 0):
                    break
                #print("ME QUEDO DANDO VUELTAS")
                #-- IMPLEMENTACION FEDE
                pckRecibido, esACKEsperado = self.recibirPaqueteACK(entidad)
                #print(esACKEsperado)
                #if(len(self.paquetesEnVuelo) == TAM_VENTANA and esACKEsperado == False):
                    #continu

                # -- VERIFICACION DE ACK --
                if (esACKEsperado) : #SI RECIBO UN ACK, SIGNIFICA QUE RECIBI EL ACK DEL ULTIMO PAQUETE QUE LLEGO BIEN
                                            # (ES DECIR QUE, TODOS LOS PAQUETES ANTERIORES TMB LLEGARON BIEN)
                    #muevo el older_seq_number a la posicion siguiente al new_seq_number
                    print("ACK CORRECTO")
                    cant_paquetes_a_popear =  pckRecibido.obtenerSeqNumber() - self.older_seq_number 
                    self.older_seq_number = pckRecibido.obtenerSeqNumber()+1
                    print("DIFERENCIA ES: ",cant_paquetes_a_popear)
                    for i in range(cant_paquetes_a_popear + 1 ): 
                        pck = self.paquetesEnVuelo.pop(0) #borro el paquete que llego bien (voy borrando de a uno)
                        print("SEQ NUMBER POPEADO ES: ",pck.obtenerSeqNumber())
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
                    print("\n\n SALTO EL TIMER \n\n")
                    timeout_start = time.time()
                    for pck in self.paquetesEnVuelo:
                        entidad.enviarPaquete(self.gestorPaquetes.pasarPaqueteABytes(pck))
            print("Cantidad paquetes en vuelo: ", len(self.paquetesEnVuelo))
            self.enviar_fin(entidad)
            conexion_cerrada,pck_recibido = self.enviar_fin(entidad)
            if(conexion_cerrada == True):
                print("CONEXION CERRADO CON EXITO")
            return
    
    def enviar_fin(self,entidad):
        pck = self.gestorPaquetes.crearPaqueteFin()
        pckBytes = self.gestorPaquetes.pasarPaqueteABytes(pck)
        print("Mensaje de fin es: ",pckBytes)
        entidad.enviarPaquete(pckBytes)
        cantidad_intentos = 1
        print("\n--El mensaje a enviar es: ", "FIN")
        print("\n-cantidad intentos es ", cantidad_intentos)

        paqueteRecibido = entidad.recibirPaquete()
        print("Recibi: ",paqueteRecibido)
        while(paqueteRecibido == None and cantidad_intentos <= 3):
            print("\n\n El paquete recibido es de tipo ", paqueteRecibido)
            entidad.enviarPaquete(pckBytes)
            paqueteRecibido = entidad.recibirPaquete()
            cantidad_intentos += 1
            print("\n--El mensaje a enviar es: ", "FIN")
            print("\n-cantidad intentos es ", cantidad_intentos)
        
        if(cantidad_intentos > 3):
            return (False,None)
        return (True,paqueteRecibido)

        


   

"""
El cliente solo va a necesitar un solo timer del paquete en vuelo mas antiguo, cuando se agota el tiempo de espera el cliente
retransmite el paquete N y todos los sucesivos a el. 

Cada vez que recibe un paquete, va a enviar un ACK de los paquetes recibidos correctamente hasta el momento que tiene 
el numero de secuencia mas alto.

"""