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

import zmq
import sys
import os 

who_is = sys.argv[1].lower() 
port = 3526 or sys.argv[2]
context = zmq.Context()


brd = [ ['']*3 for _ in range(3) ]



def clear_console():
    os.system("cls")


def game_is_started(response, player):
    print(f'{player}: {response}')
    if player == 'server': 
        if response == b'Y' or response == b'y':
            print('We are goin to play!!')
            return True
        else:
            print('Maybe the next time :(')
            return False

    else:
        if response == 'Y' or response == 'y':
            print('We are goin to play!!')
            return True
        else:
            print('Seems like you dont want play')
  


def initial_board():
    act_brd = (f'''
              0     1     2
            _____ _____ _____        
        0   |   | |   | |   |
             ¯¯¯   ¯¯¯   ¯¯¯
            _____ _____ _____        
        1   |   | |   | |   |
             ¯¯¯   ¯¯¯   ¯¯¯
            _____ _____ _____        
        2   |   | |   | |   |
             ¯¯¯   ¯¯¯   ¯¯¯
         ''')
    return (act_brd)

       


def ask_coordinates():
    #       0 <= n <= 2     mayor igual 0 && menor igual 2
    row = int(input('''In which *ROW* do you want put your token?
    >>> '''))
    col = int(input('''In which *COLUMN* do you want put your token?
    >>> '''))

    if not 0 <= row <= 2 or not 0 <= col <= 2:
        print('Please numbers between 0 and 2')
        ask_coordinates()


    return row, col
     


def update_board(token, coordinates):
   
    row = int(coordinates[0])
    col = int(coordinates[1])

    brd[row][col] = token
    act_brd = (f'''
              0     1     2
            _____ _____ _____        
        0   | {brd[0][0]} | | {brd[0][1]}  | | {brd[0][2]}  |
             ¯¯¯   ¯¯¯   ¯¯¯
            _____ _____ _____
        1   | {brd[1][0]} | | {brd[1][1]}  | | {brd[1][2]}  |
             ¯¯¯   ¯¯¯   ¯¯¯
            _____ _____ _____
        2   | {brd[2][0]} | |  {brd[2][1]} | | {brd[2][2]}  |
             ¯¯¯   ¯¯¯   ¯¯¯
         ''')
    return act_brd


def send(token, coordinates):
    info = f'{token}{coordinates}'
    socket.send_string(info)


def recieve():
    new_move = socket.recv_string()
    return new_move










if who_is == 'client':
    print('Im the client')
    player = 'client'

    #connect with the host
    socket = context.socket(zmq.REP)
    socket.bind(f'tcp://*:{port}')
      
    #server asks if client want to play
    received_q = socket.recv() 
    print(f'Server: {received_q.decode("utf-8")}')

    #response to play
    response_to_play = input('>>> ')
    socket.send(response_to_play.encode('utf-8'))
    
    if game_is_started(response_to_play, player) is True:
        print(response_to_play, player)
        #you want play
        server_starts =  socket.recv()
        print(f'{server_starts.decode("utf-8")} and Client use the [X] sign . . .')
        

        token = 'X'
        turn = 0
        print(initial_board())

    else: socket.close()

    
    
   

    

        
    
###
elif who_is == 'server':
    print('Im the server')
    player = 'server'
    #connect to the host
    socket = context.socket(zmq.REQ)
    socket.connect(f'tcp://localhost:{port}')
    
    #ask to play
    socket.send_string('Hey!, Do you want to play? [y/n]')
    response_to_play = socket.recv()
    print(f'Client: {response_to_play.decode("utf-8")}')

    #check the response
    if game_is_started(response_to_play, player) is True:

        socket.send_string('Server goes first and play with [O]')

        token = 'O'
        turn = 1
   
        print('I go first and play with [O] sign . . .')
        print(initial_board())

    else: socket.close()


        
else:
    print('I do not know who I am :(')




while True and turn < 10:

    if turn % 2 != 1:
        print('My turn', token)

    
        #need to be updated for eache turn
        coordinates = ask_coordinates()
        movement = update_board(token, coordinates)
        print(movement)

        #send my move to the board for my oponent
        send(token, coordinates)

  

    else:
        print('Oponents turn, waiting')
        print('. . . ')

        #movement of my oponent
        last_move = recieve()
        print(last_move)
      
        coordinates = [last_move[2], last_move[5]]

        actual_board = update_board(last_move[0], coordinates)
        print(actual_board)
        

    if turn == 10:
        print('Is a tie!')
        break

    turn += 1
