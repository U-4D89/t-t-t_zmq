import sys
import zmq
import os

whois = sys.argv[1]
port = sys.argv[2]
context = zmq.Context()


def iniciojuego(confirmacion):
    if confirmacion == b'S':
        print('Genial!')
        return True

    else:
        print('Sera la proxima!')
        return False


# def escoger_ficha():
#     ficha = input('Con que ficha vas a jugar? >>> ')
#     if ficha == 'O' or ficha == 'o':
#         socket.send(b'Sere [X] y tu [O]')
#         return ficha.upper()

#     elif ficha == 'X' or ficha == 'x':
#         socket.send(b'Sere [O] y tu [X]')
#         return ficha.upper()
    
#     else:
#         print('Esa ficha no juega.')
#         socket.send(b'La ficha no era valida.')
#         return False


def tablerod():
    t = [[' ']* 3 for i in range(3) ]
    print(f'''
            0     1     2
           _____ _____ _____        
        0  | {t[0][0]} | | {t[0][1]} | | {t[0][2]} |
            ¯¯¯   ¯¯¯   ¯¯¯
           _____ _____ _____
        1  | {t[1][0]} | | {t[1][1]} | | {t[1][2]} |
            ¯¯¯   ¯¯¯   ¯¯¯
           _____ _____ _____
        2  | {t[2][0]} | | {t[2][1]} | | {t[2][2]} |
            ¯¯¯   ¯¯¯   ¯¯¯
        ''')
  



def ubicarficha(ficha):
    print(f'Juega: {ficha}')
    t = [[' ']* 3 for i in range(3) ]
    fila = int(input('En que Fila va a ir esta ficha? >>>'))
    columna = int(input('En que Columna va a ir esta ficha? >>>'))
    t[fila][columna] = ficha
    print(f'''
             0     1     2
           _____ _____ _____        
        0  | {t[0][0]} | | {t[0][1]} | | {t[0][2]} |
            ¯¯¯   ¯¯¯   ¯¯¯
           _____ _____ _____
        1  | {t[1][0]} | | {t[1][1]} | | {t[1][2]} |
            ¯¯¯   ¯¯¯   ¯¯¯
           _____ _____ _____
        2  | {t[2][0]} | | {t[2][1]} | | {t[2][2]} |
            ¯¯¯   ¯¯¯   ¯¯¯
        ''')

    


if whois == 'servidor':
    print('soy servidor')
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{port}")

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

    #ficha Cliente
    fichaC = 'X'
   
    #pintar tablero para mi 
    tablerod()

    #donde ubico mi ficha?
    ubicarficha(fichaC)


elif whois == 'cliente':
    print('soy cliente')
    
    #  Socket to talk to server
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://localhost:{port}")

    #Coneccion establecida, esperando por confirmacion
    socket.send(b"Hola, quieres jugar triki SI o NO [S/N]?")
    confirmacion = socket.recv()
    print(confirmacion.decode('utf-8'))

    #Confirmacion positiva, escoger quien empieza
    if iniciojuego(confirmacion):
        socket.send(b'Voy primero!')

        #ficha Servidor
        fichaS = 'O'

        #ficha Cliente
        fichaC = 'X'
        
       
        #pintar tablero para mi 
        tablerod()

        #escoger donde va mi ficha
        ubicarficha(fichaS)


    
else:
    print('no se que quien soy :c.')
