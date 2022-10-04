import os
import cliente, stopAndWait, goBackN #nombre del archivo
import getopt
import sys
import logging
import gestorPaquetes
import sender_stop_wait
import sender_gobackn
import receiver

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
    #sender_stop = sender_stop_wait.StopWait("localhost", 9000,"lp_desde_cliente.pdf", "/home/fede/Desktop/distribuidos/alternativa_2/Intro-a-Sistemas-Distribuidos-TP1/lib/BDD_Cliente")
    #sender_stop.enviar_archivo()
    sender_goback = sender_gobackn.GoBackN("localhost", 9000,"lp_desde_cliente.pdf", "/home/fede/Desktop/distribuidos/alternativa_2/Intro-a-Sistemas-Distribuidos-TP1/lib/BDD_Cliente")
    client = cliente.Cliente("localhost", 9000, None) 
    rta = client.enviar_archivo(sender_goback)
 
main()
   