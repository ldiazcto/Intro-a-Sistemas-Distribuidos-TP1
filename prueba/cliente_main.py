import cliente


def main():
    cliente_prueba = cliente.Cliente()
    print ("Escriba mensaje")
    mensaje = input()
    cliente_prueba.mandarPaquete(mensaje)

main()