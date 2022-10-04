# Intro-a-Sistemas-Distribuidos-TP1
Trabajo Práctico N°1 de la materia Introducción a los Sistemas Distribuidos

## Ejecutar

Por default el protocolo seteado es StopAndWait para Cliente y Servidor.

Si se agrega la option -o se cambia al protocolo Go Back N

### Start-Server

```
python3 -u menuServer.py --start-server  -s <path de la ruta /lib/BDD_Servidor> -H localhost -p 9000 -o GN
```

### Download 
```
python3 -u menuCliente.py --download -d <path de /lib/BDD_Cliente> -n <nombre del archivo a descargar> -H localhost -p 9000
```

### Upload 
```
python3 -u menuCliente.py --upload -s  <path de /lib/BDD_Cliente> -n <nombre del archivo a subir> -H localhost -p 9000 -o gbn
```

## Lineas de comando

## Cliente-Upload

```
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
```

## Cliente-Download
```
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
```
## Server

```
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
```


