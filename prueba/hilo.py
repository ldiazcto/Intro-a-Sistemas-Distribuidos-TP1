import threading



class MyThread(threading.Thread):
    def __init__(self,numero_hilo, conexion_cliente):
        threading.Thread.__init__(self)
        self.nombre = numero_hilo
        self.conexion_cliente = conexion_cliente
        self.queue = []
        self.hay_data = False

    def pasar_data(self, paquete):
        self.queue.append(paquete)
        self.hay_data = True

    def run(self):
        while True:
            if self.hay_data: #verifico si me pasaron nueva data
                val = self.queue.pop(0) #obtengo la data
                if len(self.queue) == 0:
                    self.hay_data = False #si la cola queda vacia establezco que no hay mas data, por ahora
                if val is None:   # If you send `None`, the thread will exit.
                    return
                self.imprimir_mensaje(val)

    def imprimir_mensaje(self, message):
        print ("Numero_hilo:",self.nombre,"conexion:",self.conexion_cliente)
        print ("Mensaje:",message)

