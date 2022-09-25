import cliente_2


def main():
    cliente_prueba = cliente_2.Cliente()
    sequence = (1).to_bytes(2,byteorder="big")
    ack = (1).to_bytes(2,byteorder="big")
    data = (3).to_bytes(20,byteorder="big")


    paquete = sequence
    paquete += ack
    paquete += data

    cliente_prueba.mandarPaquete(paquete)
    cliente_prueba.chequearSiLlegoACK()
    

main()