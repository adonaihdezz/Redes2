# server.py
import socket
import random

def imprimir_tablero(tablero):
    n = len(tablero)
    columnas = '   ' + ' '.join(chr(65 + i) for i in range(n))
    print(columnas)

    for i in range(1, n + 1):
        print(f"{i:2} " + ' '.join(tablero[i - 1]))

def jugadas(tablero, coordenada, jugador):
    try:
        columna, fila = coordenada[0], coordenada[1]
        fila = int(fila) - 1
        columna = ord(columna.upper()) - 65
        if tablero[fila][columna] in ['X', 'O']:
            return False
        tablero[fila][columna] = jugador
        print(f"El cliente [X] juega en: ({chr(65 + columna)},{fila + 1})")
        return True
    except:
        return False

def jugada_server(tablero, jugador):
    n = len(tablero)
    casillas_libres = [(fila, columna) for fila in range(n) for columna in range(n) if tablero[fila][columna] == '.']
    if casillas_libres:
        fila, columna = random.choice(casillas_libres)
        tablero[fila][columna] = jugador
        print(f"El servidor [O] juega en: ({chr(65 + columna)},{fila + 1})")


def verificar_ganador(tablero, jugador):
    n = len(tablero)

    # Verificar filas
    for fila in tablero:
        if all(celda == jugador for celda in fila):
            return True

    # Verificar columnas
    for col in range(n):
        if all(tablero[fila][col] == jugador for fila in range(n)):
            return True

    # Verificar diagonal principal
    if all(tablero[i][i] == jugador for i in range(n)):
        return True

    # Verificar diagonal secundaria
    if all(tablero[i][n - 1 - i] == jugador for i in range(n)):
        return True

    return False


def verificar_empate(tablero):
    return all(celda != '.' for fila in tablero for celda in fila)


def iniciar_servidor():

    print("Elige la dificultad: 1. Principiante (3x3) o 2. Avanzado (5x5)")
    opcion = input("Opción: ").strip()

    if opcion == "1":
        respuesta = [['.' for _ in range(3)] for _ in range(3)]
    elif opcion == "2":
        respuesta = [['.' for _ in range(5)] for _ in range(5)]
    else:
        print("Opción no válida.")
        return
    print("Esperando conexión del cliente...")
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(("localhost", 12345))
    servidor.listen(1)
    conexion, direccion = servidor.accept()
    print(f"Conexión establecida con {direccion}")
    conexion.sendall(f"Conexión establecida con el server, dificultad: {opcion}".encode('utf-8'))

    imprimir_tablero(respuesta)
    conexion.sendall(str(respuesta).encode('utf-8'))
    while True:
        mensaje = conexion.recv(1024).decode('utf-8')
        if not mensaje:
            break

        if not jugadas(respuesta, mensaje, 'X'):
            conexion.sendall("Movimiento inválido".encode('utf-8'))
        else:
            imprimir_tablero(respuesta)
            conexion.sendall(str(respuesta).encode('utf-8'))

            if verificar_ganador(respuesta, 'X'):
                conexion.sendall("Gano el cliente".encode('utf-8'))
                break
            if verificar_empate(respuesta):
                conexion.sendall("Empate".encode('utf-8'))
                break
            jugada_server(respuesta, 'O')
            imprimir_tablero(respuesta)


            if verificar_ganador(respuesta, 'O'):
                conexion.sendall("Gano el servidor".encode('utf-8'))
                break
            if verificar_empate(respuesta):
                conexion.sendall("Empate".encode('utf-8'))
                break

    conexion.close()
    servidor.close()

if __name__ == "__main__":
    iniciar_servidor()
