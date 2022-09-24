import cliente


def main():
    cliente_prueba = cliente.Cliente()
    while True:
        print ("Escriba mensaje")
        mensaje = input()
        cliente_prueba.mandarPaquete(mensaje)

main()