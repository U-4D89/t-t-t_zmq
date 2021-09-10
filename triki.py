'''
1 - preguntar quien esta jugando 
    - ver whois
    - posibles jugadores: servidor cliente

2 - confirmar si se desea jugar
    - ver la funcion iniciojuego
    - posibles opciones: NO, no desean jugar
                         SI, juguemos 


3 - Escoger fichas para cada jugador, por defecto:
        [ X ]  -- Cliente
        [ O ]  -- Servidor


4 - Decidir quien va primero, por defecto
        Cliente, sera siempre impar, iniciar turno en 1
        una vez terminado el turno, sumar 1 para que sea
        para par y sea el turno del servidor


5 - dibujar tablero debe ser de 3 x 3
    - ver variable [t]

6 - Un turno se determina cuando
    - se pregunta por una fila
    - se pregunta por una columna
    - con fila y columna, ubicar en el tablero

    ***Es posible que en algun momento se quiera colocar una 
        ficha donde ya la hay pero, el juego no lo permite, 

        Como saber si una posicion  es valida?
        ~ Porque lo que hay alli no es diferente de espacio  = ' '

7 - Cuando los turnos sean mayores de 3
    empezar a buscar si hay fichas iguales en las posiciones
    horizontales [0,0  0,1  0,2], [1,0  1,1  1,2], [2,0  2,1  2,2], 
    verticales [0,0  1,0  2,0], [0,1  1,1  2.1], [0,2  1,2  2,2],
    diagonales [0,0  1,1  2,2], [ 0,2  1,1  2,0 ]
    para determinar si ganador

8 - Si hay un ganador, el juego deberia terminar pero, que pasa si
    no hay un ganador?
    ***El juego determinara empate cuando el tablero este lleno, 
    ~ Como saberlo?
        Mirar casilla por casilla, 
        si hay casillas que no contengan espacios = ' '
'''

import sys
import zmq
from os import system

whois = sys.argv[1]
port = sys.argv[2]
context = zmq.Context()



#tablero
t = [[' ']* 3 for i in range(3) ]

def iniciojuego(confirmacion):
    if confirmacion == b'S':
        print('Genial!, Vamos a jugar')
        return True

    else:
        print('Sera la proxima!')
        return False

def posicion():
    fila = int(input('Fila en la que deseas ubicar tu ficha? >>> '))
    columna = int(input('Columna en la que deseas ubicar tu ficha? >>> '))
    return fila, columna
    # tablero = act_tab(ficha, fila, columna)
    # EnviarStatus(tablero)

def act_tab(ficha, fila, columna):
    t[fila][columna] = ficha
    tab = (f'''
              0     1     2
            _____ _____ _____        
         0  | {t[0][0]} | | {t[0][1]} | | {t[0][2]} |
             ¯¯¯   ¯¯¯   ¯¯¯
            _____ _____ _____
         1  | {t[1][0]} | | {t[1][1]} | | {t[1][2]} |
             ¯¯¯   ¯¯¯   ¯¯¯
            _____ _____ _____
        2   | {t[2][0]} | | {t[2][1]} | | {t[2][2]} |
             ¯¯¯   ¯¯¯   ¯¯¯
         ''')
    return (tab)
    
def EnviarStatus(tablero):
    tc = tablero.encode('utf-8')
    socket.send(tc)
    #RecibirStatus(tc)


def RecibirStatus():
    #Recibe Tablero Codificado (tc)
    tc = socket.recv()
    td = tc.decode('utf-8')
    print(td)

if whois == 'servidor':
    print('soy servidor')
    jugador = 'servidor'
    turno = 1
    socket = context.socket(zmq.REP)
    socket.bind(f'tcp://*:{port}')

    #coneccion establecida
    saludo = socket.recv()
    print(f'Recibi esto: {saludo}')

    #enviar respuesta (quiero jugar si o no?)
    confirmacion = input('>>> ')
    socket.send(confirmacion.encode('utf-8'))

    #quien empieza?
    empieza = socket.recv()
    print(f'Recibi esto: {empieza}')
    
    #ficha Servidor
    fichaS = 'O'

    #enviar la asignacion de fichas
    asignacion = 'Está bien, pero yo {servidor} juego con [O] y tú {cliente} juegas con [X].'
    socket.send(asignacion.encode('utf-8'))

    while True:
        if turno % 2 != 0:
           #voy a ver que jugada hizo mi oponente
            RecibirStatus()
            turno =+1
        else:
            #es mi turno, voy a colocar mi ficha 
            posicion(fichaS)
            
           
        

elif whois == 'cliente':
    print('soy cliente')
    jugador = 'cliente'
    turno = 1

    #  Socket to talk to server
    socket = context.socket(zmq.REQ)
    socket.connect(f'tcp://localhost:{port}')

    socket.send(b'Hola, quieres jugar triki SI o NO [S/N]?')
    confirmacion = socket.recv()
    print(confirmacion.decode('utf-8'))

    #Confirmacion positiva, escoger quien empieza
    if iniciojuego(confirmacion):
        socket.send(b'Voy primero!')

        #ficha Cliente
        fichaC = 'X'
        
        #fichas asignadas
        asignacion = socket.recv()
        print(asignacion.decode('utf-8'))

        while True:
            if turno % 2 != 0:
                #es mi turno, voy a colocar mi ficha
                coor  = posicion()
                print(coor[0])

                #tablero
                move = act_tab(fichaC, coor[0], coor[1])
                print(move)

                #enviar jugada a mi oponente
                EnviarStatus(move)
                turno =+1
            else: 
                #voy a ver que jugada hizo mi oponente
                RecibirStatus()
            #print(t)
    
else:
    print('no se que quien soy :c.')
