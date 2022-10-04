# Intro-a-Sistemas-Distribuidos-TP1
Trabajo Práctico N°1 de la materia Introducción a los Sistemas Distribuidos

Lineas de comando

Cliente-Upload

> python upload -h
usage : upload [-h] [-v | -q] [-H ADDR ] [-p PORT ] [-s FILEPATH ] [-n FILENAME ]
<command description >
optional arguments :
-h, --help show this help message and exit
-v, -- verbose increase output verbosity
-q, --quiet decrease output verbosity
-H, --host server IP address
-p, --port server port
-s, --src source file path
-n, --name file name
-o, --option select protocol

Cliente-Download

> python download -h
usage : download [-h] [-v | -q] [-H ADDR ] [-p PORT ] [-d FILEPATH ] [-n FILENAME ]
<command description >
optional arguments :
-h, --help show this help message and exit
-v, -- verbose increase output verbosity
-q, --quiet decrease output verbosity
-H, --host server IP address
-p, --port server port
-d, --dst destination file path
-n, --name file name
-o, --option select protocol

Server

> python start - server -h
usage : start - server [-h] [-v | -q] [-H ADDR ] [-p PORT ] [-s DIRPATH ]
<command description >
optional arguments :
-h, --help          show this help message and exit
-v, -- verbose      increase output verbosity
-q, --quiet         decrease output verbosity
-H, --host          service IP address
-p, --port          service port
-s, -- storage      storage dir path
-o, --option        select protocol

Ejecutar

Start-Server

python3 menuServer.py --start-server -v -h (server IP adress) -p (service port) -s (storage dir path) -o (protocolo)

python3 menuCliente.py --upload -s ./lib/ -n "hola.txt" -h (addr) -p (port) 


