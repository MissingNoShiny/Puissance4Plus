# coding: utf-8

import json
import random
from enum import Enum
from typing import List, Optional, Tuple


class Player:
    """
    Classe utilisée pour représenter un joueur
    """

    NEUTRAL_COLOR = "#fff"

    def __init__(self, name: str, color: str, is_ai: bool = False):
        """
        :param name: Le nom du joueur
        :param color: La couleur du joueur sous forme d'un tuple RGB
        :param is_ai: Une valeur booléenne indiquant si le joueur est contrôlé par l'ordinateur
        """
        self.name: str = name
        self.color: str = color
        self.is_ai = is_ai

    def __str__(self):
        return f"Joueur {self.name} ({'ordi' if self.is_ai else 'humain'})"


class BoardState(Enum):
    """
    Énumération utilisée pour représenter l'état de la partie : en cours, gagnée ou égalité
    """
    RUNNING = 0
    WON = 1
    DRAW = 2


class Effect(Enum):
    """
    Énumération utilisée pour représenter les différents effets possibles lors
    """
    NONE = 0
    PLAY_TWICE = 1
    REMOVE_ROW = 2
    REMOVE_COLUMN = 3
    POP_BOTTOM = 4
    EMPTY_BOARD = 5
    NEUTRAL_CHIP = 6

    _weights = [
        40,
        10,
        12,
        12,
        12,
        2,
        12
    ]

    @staticmethod
    def generate_effect():
        """
        Génère aléatoirement un effet, en fonction des poids assignés à chaque
        :return:
        """
        choices = [effect.value for effect in Effect[:-1]]
        return random.choices(choices, weights=Effect._weights)


class Board:
    """
    Classe utilisée pour représenter le plateau de jeu
    """

    def __init__(self, players: List[Player], width: int = 7, height: int = 6, win_condition: int = 4,
                 time_limit: int = 0):
        """
        :param players: Une liste d'objets Player représentant la liste des joueurs
        :param width: La largeur du plateau de jeu
        :param height: La hauteur du plateau de jeu
        :param win_condition: Le nombre de pions à aligner pour gagner la partie
        :param time_limit: Le temps limite pour jouer chaque coup, en secondes
        """
        self.grid: List[List[Optional[Player]]] = [[None for _ in range(width)] for _ in range(height)]

        self.players: List[Player] = players
        self.current_player_index: int = 0
        self.win_condition: int = win_condition
        self.state: BoardState = BoardState.RUNNING
        self.turn_count = 0
        self.current_effect = Effect.NONE
        self.time_limit = time_limit

    @property
    def width(self) -> int:
        """
        La largeur du plateau de jeu
        """
        return len(self.grid[0])

    @property
    def height(self) -> int:
        """
        La hauteur du plateau de jeu
        """
        return len(self.grid)

    @property
    def current_player(self) -> Player:
        """
        Le joueur dont c'est le tour
        :return: Un objet Player représentant le joueur dont c'est le tour
        """
        return self.players[self.current_player_index]

    @property
    def non_full_columns(self) -> List[int]:
        """
        Retourne une liste des colonnes non pleines
        """
        return [column for column in range(self.width) if not self.is_full(column)]

    def randomize_order(self) -> None:
        """
        Mélange la liste des joueurs pour rendre l'ordre de jeu aléatoire
        """
        random.shuffle(self.players)

    def next_player(self) -> None:
        """
        Passe le tour de jeu au joueur suivant
        """
        if self.turn_count > 0:
            self.turn_count -= 1
        else:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def get_height(self, column_index: int) -> int:
        """
        Calcule le nombre de pions contenus dans une colonne
        :param column_index: L'index de la colonne
        :return: Le nombre de pions qu'elle contient
        """
        return len([x for x in [row[column_index] for row in self.grid] if x is not None])

    def is_full(self, column_index: int) -> bool:
        """
        Détermine si une colonne est pleine de pions
        :param column_index: L'index de la colonne
        :return: True si la colonne est pleine, False sinon
        """
        return self.get_height(column_index) == self.height

    def place(self, column_index: int, neutral: bool = False) -> None:
        """
        Place un pion appartenant au joueur dont c'est le tour dans une colonne
        :param neutral: Si True, place un pion n'appartenant à aucun joueur à la place
        :param column_index: L'index de la colonne dans laquelle placer le pion
        """
        if self.state != BoardState.RUNNING:
            return  # TODO: Erreur?
        if self.is_full(column_index):
            return  # TODO: Erreur
        row = self.get_height(column_index)
        if neutral:
            self.grid[row][column_index] = Player("", Player.NEUTRAL_COLOR)
            return
        self.grid[row][column_index] = self.current_player

        if self.current_effect is not None:
            self.apply_effect(row, column_index)
        if self.check_win(row, column_index):
            self.state = BoardState.WON
            return
        if self.check_draw():
            self.state = BoardState.DRAW
            return
        self.next_player()

    def get_player_at(self, row: int, col: int) -> Optional[Player]:
        """
        Récupère le joueur propriétaire du pion aux coordonnées spécifiées
        :param row: La rangée du pion
        :param col: La colonne du pion
        :return: Un objet Player représentant le joueur dont le pion est à l'emplacement spécifié, None s'il n'y a pas
        de joueur à cet emplacement dans la grille ou que l'emplacement se situe en dehors de la grille
        """
        return None if not (0 <= row < self.height and 0 <= col < self.width) else self.grid[row][col]

    def check_win(self, row: int, col: int) -> bool:
        """
        Détermine si le pion aux coordonnées spécifiées fait partie d'une série gagnante
        :param row: La rangée du pion
        :param col: La colonne du pion
        :return: True si le pion fait partie d'une série gagnante, False sinon
        """
        player = self.get_player_at(row, col)
        if player is None:
            return False
        for direction in [(1, 0), (1, 1), (0, 1), (-1, 1)]:
            for i in range(self.win_condition):
                if len({self.get_player_at(row - (i - j) * direction[0],
                                           col - (i - j) * direction[1]) for j in range(self.win_condition)}) == 1:
                    return True
        return False

    def check_draw(self):
        """
        Détermine si le plateau de jeu est rempli. Si c'est le cas, on suppose que c'est une égalité.
        :return:
        """
        return len(self.non_full_columns) == 0

    def remove_column(self, column_index: int) -> None:
        """
        Supprime les pions d'une colonne du plateau
        :param column_index: L'index de la colonne
        """
        for row in range(self.height):
            self.grid[row][column_index] = None

    def remove_row(self, row_index: int) -> None:
        """
        Supprime les pions d'une rangée du plateau
        :param row_index:  L'index de la rangée
        """
        for column in range(self.width):
            self.grid[row_index][column] = None
            self.apply_gravity(column)

    def remove_bottom_chip(self, column_index: int) -> None:
        """
        Supprime le pion le plus bas d'une colonne
        :param column_index: L'index de la colonne
        """
        self.grid[0][column_index] = None
        self.apply_gravity(column_index)

    def apply_gravity(self, column_index: int) -> None:
        """
        Applique de la gravité dans une colonne, càd fait descendre chaque pion de cette colonne jusqu'à
        l'emplacement vide le plus bas sous le pion
        :param column_index: L'index de la colonne sur laquelle appliquer la gravité
        """
        new_column = sorted([self.grid[row][column_index] for row in range(self.height)], key=lambda x: x is None)
        for row, player in enumerate(new_column):
            self.grid[row][column_index] = player

    def empty_board(self) -> None:
        """
        Vide entièrement le plateau de jeu
        """
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]

    def give_extra_turn(self) -> None:
        """
        Donne un tour supplémentaire au joueur dont c'est le tour
        """
        self.turn_count += 1

    def add_neutral_chip(self) -> None:
        """
        Ajoute un pion neutre dans une colonne aléatoire
        """
        self.place(random.choice(self.non_full_columns), neutral=True)

    def apply_effect(self, row: int, column: int) -> None:
        """
        Applique l'effet actuel sur la grille de jeu
        :param row: La rangée sur laquelle appliquer l'effet
        :param column: La colonne sur laquelle appliquer l'effet
        """
        if self.current_effect == Effect.PLAY_TWICE:
            self.give_extra_turn()
        elif self.current_effect == Effect.REMOVE_ROW:
            self.remove_row(row)
        elif self.current_effect == Effect.REMOVE_COLUMN:
            self.remove_column(column)
        elif self.current_effect == Effect.POP_BOTTOM:
            self.remove_bottom_chip(column)
        elif self.current_effect == Effect.EMPTY_BOARD:
            self.empty_board()
        elif self.current_effect == Effect.NEUTRAL_CHIP:
            self.add_neutral_chip()

    def to_dict(self) -> dict:
        grid_list = [[None if self.grid[y][x] is None else self.grid[y][x].__dict__ for x in range(self.width)]
                     for y in range(self.height)][::-1]
        print(grid_list)
        data = {
            "players": [player.__dict__ for player in self.players],
            "width": self.width,
            "height": self.height,
            "win_condition": self.win_condition,
            "current_player_index": self.current_player_index,
            "grid": grid_list,
            "current_effect": self.current_effect.value,
            "time_limit": self.time_limit,
            "state": self.state.value
        }
        return data

    def __str__(self) -> str:
        max_length = max([len(player.name) for player in self.players])
        rows = ["|".join(f"{'' if el is None else el.name:{max_length}}" for el in row) for row in self.grid]
        return f"\n{'|'.join(['-' * max_length for _ in range(self.width)])}\n".join(rows[::-1])
