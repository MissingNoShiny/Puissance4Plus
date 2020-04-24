# coding: utf-8

from __future__ import annotations

__author__ = "Mathias Billot, Xavier Hoyois, Nicolas Jeuniaux, Vincent Larcin, Maxence Manteau"
__version__ = "1.0"
__status__ = "Production"

import copy
import random

import puissance4plus.board


class AIError(Exception):
    pass


class BoardAI:

    @classmethod
    def get_move(cls, board: puissance4plus.board.Board, ai_level: int = 0) -> int:
        """
        Retourne la colonne dans laquelle un joueur ordi doit jouer
        :param board: Le plateau de jeu
        :param ai_level: Le niveau de difficulté de l'ordi, qui correspond au nombre de tours dans le futur analysés
        :return: L'index de la colonne dans laquelle jouer
        """
        if ai_level == 0:
            return random.choice(board.non_full_columns)
        else:
            if board.game_mode != puissance4plus.board.GameMode.SOLO and len(board.players) != 2:
                raise AIError
            return cls.minmax(board, ai_level)

    @classmethod
    def minmax(cls, board: puissance4plus.board.Board, depth: int) -> int:
        """
        Permet de calculer la valeur d'une situation donnée grâce à l'algorithme du minmax
        :param board: Le plateau à analyser
        :param depth: La profondeur de recherche, càd le nombre de tours dans le futur que l'algorithme analysera
        :return: Le score de la position
        """
        scores = {}
        for column in board.non_full_columns:
            new_board = copy.deepcopy(board)
            new_board.place(column)
            scores[column] = cls._minmax_rec(new_board, depth, -1000, 1000, False)
        max_score = max(scores.values())
        return random.choice([column for column in scores.keys() if scores[column] == max_score])

    @classmethod
    def _minmax_rec(cls, board: puissance4plus.board.Board, depth: int, alpha: int, beta: int, maximizing: bool) -> int:
        """
        Fonction récursive implémentant l'algorithme du minmax avec élagage alpha-bêta. Ne pas utiliser en dehors
        de la fonction cls.minmax
        """
        if board.state != puissance4plus.board.BoardState.RUNNING:
            if board.state == puissance4plus.board.BoardState.DRAW:
                return 0
            else:
                return depth+1 if board.current_player.player_type == puissance4plus.board.PlayerType.AI else -depth-1
        if depth == 0:
            return 0
        if maximizing:
            score = -1000
            for column in board.non_full_columns:
                new_board = copy.deepcopy(board)
                new_board.place(column)
                score = max(score, cls._minmax_rec(new_board, depth, alpha, beta, False))
                alpha = max(alpha, score)
                if alpha >= beta:
                    break
            return score
        else:
            score = 1000
            for column in board.non_full_columns:
                new_board = copy.deepcopy(board)
                new_board.place(column)
                score = min(score, cls._minmax_rec(new_board, depth - 1, alpha, beta, True))
                beta = min(beta, score)
                if alpha >= beta:
                    break
            return score
