import sys
import zmq


print('triki')
whois = sys.argv[1]
port = sys.argv[2]
context = zmq.Context()


def iniciojuego(confirmacion):
    if confirmacion == b'S':
        print('genial!')
        return True

    else:
        print('Sera la proxima!')
        return False

def escoger_ficha():
    ficha = input('Con que ficha vas a jugar? >>> ')
    if ficha == 'O':
        socket.send(b'Sere [O] y tu [X]')

    elif ficha == 'X':
        socket.send(b'Sere [X] y tu [O]')

    else:
        print('Esa ficha no juega.')
        socket.send(b'La ficha no era valida.')
        return False


def tablero():
    print('''
         0     1     2
       _____ _____ _____        
    0  |   | |   | |   |
        ¯¯¯   ¯¯¯   ¯¯¯
       _____ _____ _____
    1  |   | |   | |   |
        ¯¯¯   ¯¯¯   ¯¯¯
       _____ _____ _____
    0  |   | |   | |   |
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
    
    #fichas escogidas
    escoger_ficha()

    #pintar tablero para mi 
    tablero()

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

        #ficha
        socket.recv()

        #pintar tablero para mi 
        tablero()


    
else:
    print('no se que quien soy :c.')