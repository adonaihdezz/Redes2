# client.py
import socket
import ast

def imprimir_tablero(tablero):
    n = len(tablero)
    columnas = '   ' + ' '.join(chr(65 + i) for i in range(n))
    print(columnas)

    for i in range(1, n + 1):
        print(f"{i:2} " + ' '.join(tablero[i - 1]))


def main():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(('localhost', 12345))

    mensaje = cliente.recv(1024).decode('utf-8')
    print(mensaje)  # Muestra el mensaje de conexión

    while True:
        tablero = cliente.recv(1024).decode('utf-8')
        print("Tablero actual:")
        print(tablero)

        if "Gano" in tablero or "Empate" in tablero:
            print(tablero)  # Muestra el mensaje de resultado
            break

        jugada = input("Introduce tu jugada (Ejemplo: A1): ")
        cliente.sendall(jugada.encode('utf-8'))

    cliente.close()

if __name__ == "__main__":
    main()