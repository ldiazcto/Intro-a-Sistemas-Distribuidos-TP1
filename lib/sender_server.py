import threading
import abc
import time

MAX_TRIES = 3
MAX_WAIT = 3

class Sender_Server(metaclass=abc.ABCMeta):
        

        def pasar_data(self, paquete= b""):
                self.cola.append(paquete)
                self.hay_data = True
        
        def enviar_archivo(self):
                filepath= self.filePath + "/" + self.filename
                file = open(filepath,'rb')
                print("VOY A ENVIAR PAQUETES")
                self.enviarPaquetes(file)
                self.Termino = True
                file.close()
        
        def recibirPaquete(self):
                timeout_start = time.time()
                while True:
                        var = time.time()
                        if ((var - timeout_start) >= (MAX_WAIT)):
                                return None
                        if (self.hay_data == False):
                                continue
                        paqueteString = self.cola.pop(0)
                        if(len(self.cola) == 0):
                                self.hay_data = False
                        return self.gestorPaquetes.pasarBytesAPaquete(paqueteString)



        @abc.abstractmethod
        def terminar_ejecucion(self, nuevo_estado):
                pass
        
        @abc.abstractmethod
        def recibir_y_esperar(self, pckBytes):
                pass


        def enviar_fin(self,):
                pck = self.gestorPaquetes.crearPaqueteFin()
                pckBytes = self.gestorPaquetes.pasarPaqueteABytes(pck)
                self.sender_socekt.sendto(pckBytes,(self.receiver_ip,self.receiver_port))
                
                paqueteRecibido, cantidad_intentos = self.recibir_y_esperar(pckBytes)

                
                if(cantidad_intentos > MAX_TRIES):
                        self.terminar_ejecucion(True)
                        return (False,None)
                return (True,paqueteRecibido)



        @abc.abstractmethod
        def enviarPaquetes(self, file):
                pass
