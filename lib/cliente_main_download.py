import os
import cliente, stopAndWait, goBackN #nombre del archivo
import getopt
import sys
import logging
import gestorPaquetes
import sender_stop_wait
import sender_gobackn
import receiver
import cliente


SERVER_ADDR = ""
SERVER_PORT = 120
FILEPATH = ""
FILENAME = ""
UPLOAD = 2
DOWNLOAD = 3

#NIVELES DE LOGS
NOTSET = 0
DEBUG = 10
INFO = 20
WARNING = 30
CRITICAL = 50
QUIET = 51

def abrirArchivo(ruta):
        try:
            file = open(ruta,'rb')
            return file
        except FileNotFoundError: #o IOERROR o FileExistsError
            print("FILE NO ENCONTRADO")
            sys.exit(2)


def main():


    receiver_aux = receiver.Receiver("localhost", 12000, "/Users/abrildiazmiguez/Desktop/Intro_a_Distr/Intro-a-Sistemas-Distribuidos-TP1/lib/BDD_Cliente", "lp_desde_servidor.pdf")
    client = cliente.Cliente("localhost", 12000, None)
    rta = client.recibir_archivo(receiver_aux)
  
main()
   