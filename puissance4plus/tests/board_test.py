# coding: utf-8
from ..board import *


#Classe Player

def test_Player() :
    player1 = Player(name='xavier', color='(150, 150, 150)')
    assert player1.name == 'xavier'
    assert type(player1.name) is str
    assert type(player1.color) is str


#Classe BoardState

def test_BoardState() :
    etat = BoardState(1)
    assert etat.name == 'WON'


def test_Effect():
    effet = Effect(1)
    assert effet.name == 'PLAY_TWICE'


#Classe Board

def test_Board() :
    player1 = Player(name='xavier', color='(150, 150, 150)')
    player2 = Player(name='maxence', color='(150, 150, 150)')
    plateau = Board([player1, player2], 7, 6, 4)
    assert type(plateau.players) is list
    assert type(plateau.width) is int
    assert type(plateau.height) is int
    assert type(plateau.win_condition) is int
    assert plateau.win_condition == 4
    assert plateau.width == 7
    assert plateau.height == 6
    assert plateau.state.value == 0

def test_width():
    player1 = Player(name='xavier', color='(150, 150, 150)')
    player2 = Player(name='maxence', color='(150, 150, 150)')
    plateau = Board([player1, player2], 7, 6, 4)
    assert plateau.width == 7
    assert type(plateau.width) is int

def test_height():
    player1 = Player(name='xavier', color='(150, 150, 150)')
    player2 = Player(name='maxence', color='(150, 150, 150)')
    plateau = Board([player1, player2], 7, 6, 4)
    assert type(plateau.height) is int
    assert plateau.height == 6


def test_current_player():
    player1 = Player(name='xavier', color='(150, 150, 150)')
    player2 = Player(name='maxence', color='(150, 150, 150)')
    plateau = Board([player1, player2], 7, 6, 4)
    assert type(plateau.players[plateau.current_player_index]) is Player

def test_randomize_order():
    player1 = Player(name='xavier', color='(150, 150, 150)')
    player2 = Player(name='maxence', color='(150, 150, 150)')
    plateau = Board([player1, player2], 7, 6, 4)
    plateau.randomize_order()
    assert [player.name for player in plateau.players] == ['xavier', 'maxence'] or [player.name for player in plateau.players] == ['maxence', 'xavier']


def test_next_player():
    player1 = Player(name='xavier', color='(150, 150, 150)')
    player2 = Player(name='maxence', color='(150, 150, 150)')
    player3 = Player(name='mathias', color='(150, 150, 150)')
    plateau = Board([player1, player2, player3], 7, 6, 4)
    assert plateau.current_player_index == 0
    plateau.next_player()
    assert plateau.current_player_index == 1
    plateau.next_player()
    assert plateau.current_player_index == 2


def test_get_height():
    x = 2
    player1 = Player(name='xavier', color='(150, 150, 150)')
    player2 = Player(name='maxence', color='(150, 150, 150)')
    plateau = Board([player1, player2], 7, 6, 4)
    assert type(plateau.get_height(x)) is int
    assert plateau.get_height(x) == 0


def test_is_full():
    x = 2
    player1 = Player(name='xavier', color=(150, 150, 150))
    player2 = Player(name='maxence', color=(150, 150, 150))
    plateau = Board([player1, player2], 7, 6, 4)
    assert type(plateau.is_full(x)) is bool
    assert plateau.is_full(x) == False

def test_place():
    x, y, q, s = 3, 7, 0, 0
    player1 = Player(name='xavier', color='(150, 150, 150)')
    player2 = Player(name='maxence', color='(150, 150, 150)')
    plateau = Board([player1, player2], 7, 6, 4)
    for i in range(y):          #remplir ligne (choisir colonne)
        for a in range(x):      #remplir colonne (choisir ligne)
            plateau.place(i)        #placer pion
    assert plateau.grid[q][s] == player1 or plateau.grid[q][s] == player2  #choisir case à verrifier


def test_get_player_at():
    x, y, q, s = 3, 7, 0, 1
    player1 = Player(name='xavier', color='(150, 150, 150)')
    player2 = Player(name='maxence', color='(150, 150, 150)')
    plateau = Board([player1, player2], 7, 6, 4)
    for i in range(y):          #remplir ligne (choisir colonne)
        for a in range(x):      #remplir colonne (choisir ligne)
            plateau.place(i)        #placer pion
    assert type(plateau.get_player_at(q, s)) is Player
    assert plateau.get_player_at(q, s).name == player1.name or plateau.get_player_at(q, s).name == player2.name

def test_check_win():
    x, y, q, s = 3, 7, 0, 3
    player1 = Player(name='xavier', color='(150, 150, 150)')
    player2 = Player(name='maxence', color='(150, 150, 150)')
    plateau = Board([player1, player2], 7, 6, 4)
    for i in range(y):  # remplir ligne (choisir colonne)
        for a in range(x):  # remplir colonne (choisir ligne)
            plateau.place(i)  # placer pion
    assert type(plateau.check_win(q, s)) is bool
    assert plateau.check_win(q, s) == False
    plateau.place(0)
    assert plateau.check_win(q, s) == True

def test_remove_column():         #experimentation
    x, y = 3, 7
    f = 3               #index colonne à delete
    z = 0
    player1 = Player(name='xavier', color='(150, 150, 150)')
    player2 = Player(name='maxence', color='(150, 150, 150)')
    plateau = Board([player1, player2], 7, 6, 4)
    for i in range(y):  # remplir ligne (choisir colonne)
        for a in range(x):  # remplir colonne (choisir ligne)
            plateau.place(i)  # placer pion
    plateau.remove_column(f)
    while z < x:
        assert plateau.grid[z][f] == None
        z += 1

def test_remove_row():          #experimentation
    x, y = 3, 7                 #hauteur, longueur
    f = 1                       # index ligne à delete
    z, j = 0, 0                 #pour les boucles
    avant = []                  #liste avant remove
    apres = []                  #liste apres remove
    player1 = Player(name='xavier', color='(150, 150, 150)')
    player2 = Player(name='maxence', color='(150, 150, 150)')
    plateau = Board([player1, player2], 7, 6, 4)
    for i in range(y):          # remplir ligne (choisir colonne)
        for a in range(x):      # remplir colonne (choisir ligne)
            plateau.place(i)    # placer pion
    while z < y:
        avant.append(plateau.grid[f+1][z])
        z += 1
    plateau.remove_row(f)
    while j < y:
        apres.append(plateau.grid[f][j])      #retirer +1 si gravity activate
        j += 1
    assert avant == apres

def test_remove_chip():         #experimentation
    x, y = 3, 7         # hauteur, longueur
    f = 1               # index colonne à delete la case du bas
    z, j = 0, 0         # pour les boucles
    avant = []          # liste avant remove
    apres = []          # liste apres remove
    player1 = Player(name='xavier', color='(150, 150, 150)')
    player2 = Player(name='maxence', color='(150, 150, 150)')
    plateau = Board([player1, player2], 7, 6, 4)
    for i in range(y):          # remplir ligne (choisir colonne)
        for a in range(x):      # remplir colonne (choisir ligne)
            plateau.place(i)    # placer pion

    while z < x - 1:
        avant.append(plateau.grid[z+1][f])
        z += 1
    plateau.remove_bottom_chip(f)
    while j < x - 1:
        apres.append(plateau.grid[j][f])
        j += 1
    assert avant == apres

def test_empty_board():         #experimentation
    x, y = 3, 7             # hauteur, longueur
    j = 0                   # pour les boucles
    apres = []              # liste apres remove
    player1 = Player(name='xavier', color='(150, 150, 150)')
    player2 = Player(name='maxence', color='(150, 150, 150)')
    plateau = Board([player1, player2], 7, 6, 4)
    for i in range(y):                  # remplir ligne (choisir colonne)
        for a in range(x):              # remplir colonne (choisir ligne)
            plateau.place(i)            # placer pion
    plateau.empty_board()
    while j < y:
        assert plateau.grid[0][j] == None
        j += 1