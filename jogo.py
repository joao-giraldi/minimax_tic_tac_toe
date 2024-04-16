from math import inf as infinity
from random import choice
import platform
from os import system

HUMAN = -1
COMP = +1
jogo = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]


def verificar(jogo):
    #Função para verificar se alguem ganhou, primoridalmente vai ser chamada na função minimax
    #Se o computador ganhar, a pontuação é +1
    #Se o computador perder, a pontuação é -1
    #Caso contrário, a pontuação é 0
    if ganhou(jogo, COMP):
        score = +1
    elif ganhou(jogo, HUMAN):
        score = -1
    else:
        score = 0

    return score


def ganhou(jogo, player):
    #Função para verificar se determinado jogador venceu
    vitoria = [
        [jogo[0][0], jogo[0][1], jogo[0][2]],
        [jogo[1][0], jogo[1][1], jogo[1][2]],
        [jogo[2][0], jogo[2][1], jogo[2][2]],
        [jogo[0][0], jogo[1][0], jogo[2][0]],
        [jogo[0][1], jogo[1][1], jogo[2][1]],
        [jogo[0][2], jogo[1][2], jogo[2][2]],
        [jogo[0][0], jogo[1][1], jogo[2][2]],
        [jogo[2][0], jogo[1][1], jogo[0][2]],
    ]
    if [player, player, player] in vitoria:
        return True
    else:
        return False

#Função para terminar o jogo
def game_over(jogo): return ganhou(jogo, HUMAN) or ganhou(jogo, COMP)


def espaço_vazio(jogo):
    #Função para identificar quantos e quais espaços estão vazios no tabuleiro
    cells = []
    for x, row in enumerate(jogo):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])
    return cells


def valid_move(x, y):
    #Função para verificar se determinado movimento é válido
    if [x, y] in espaço_vazio(jogo):
        return True
    else:
        return False


def set_move(x, y, player):
    #Função para definir o movimento após verificação se é válido
    if valid_move(x, y):
        jogo[x][y] = player
        return True
    else:
        return False


def minimax(jogo, depth, player):
    #Função minimax
    #Algoritmo para o computador decidir qual movimento é o melhor
    #Jogo = tabuleiro atual
    #Nodo atual da árvore
    #Player: ver quem está jogando
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(jogo):
        score = verificar(jogo)
        return [-1, -1, score]

    for cell in espaço_vazio(jogo):
        x, y = cell[0], cell[1]
        jogo[x][y] = player
        score = minimax(jogo, depth - 1, -player)
        jogo[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best


def clean():
    #Função pra limpar a tela
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def print_jogo(jogo, c_choice, h_choice):
    #Função para printar o tabuleiro
    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for row in jogo:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)


def ai_turn(c_choice, h_choice):
    #Função da jogada da IA
    depth = len(espaço_vazio(jogo))
    if depth == 0 or game_over(jogo):
        return

    clean()
    print(f'Vez da IA [{c_choice}]')
    print_jogo(jogo, c_choice, h_choice)

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(jogo, depth, COMP)
        x, y = move[0], move[1]

    set_move(x, y, COMP)


def human_turn(c_choice, h_choice):
    #Função da jogada do Jogador
    depth = len(espaço_vazio(jogo))
    if depth == 0 or game_over(jogo):
        return
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    clean()
    print(f'Vez do Jogador [{h_choice}]')
    print_jogo(jogo, c_choice, h_choice)

    while move < 1 or move > 9:
        move = int(input('Use os números de 1 a 9: '))
        coord = moves[move]
        can_move = set_move(coord[0], coord[1], HUMAN)

        if not can_move:
            print('Jogada Inválida')
            move = -1



clean()
#Definir se o jogador quer ser o X ou o O e quem joga primeiro
h_choice = ''
c_choice = ''
first = ''
while h_choice != 'O' and h_choice != 'X':
    print('')
    h_choice = input('Choose X or O\nChosen: ').upper()
if h_choice == 'X':
    c_choice = 'O'
else:
    c_choice = 'X'
clean()
while first != 'S' and first != 'N': first = input('Quer começar?[s/n]: ').upper()

#Loop principal
while len(espaço_vazio(jogo)) > 0 and not game_over(jogo):
    if first == 'N':
        ai_turn(c_choice, h_choice)
        first = ''

    human_turn(c_choice, h_choice)
    ai_turn(c_choice, h_choice)

#Fim de jogo
if ganhou(jogo, HUMAN):
    clean()
    print(f'Vez do jogador [{h_choice}]')
    print_jogo(jogo, c_choice, h_choice)
    print('Você VENCEU!')
elif ganhou(jogo, COMP):
    clean()
    print(f'Vez da IA [{c_choice}]')
    print_jogo(jogo, c_choice, h_choice)
    print('Você PERDEU!')
else:
    clean()
    print_jogo(jogo, c_choice, h_choice)
    print('EMPATE!')