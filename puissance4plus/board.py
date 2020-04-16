# coding: utf-8

import random
from enum import Enum
from typing import List, Optional, Tuple


class Player:
    def __init__(self, name: str, color: Tuple[int, int, int]):
        self.name: str = name
        self.color: Tuple[int, int, int] = color


class BoardState(Enum):
    running = 0
    won = 1
    draw = 2


class Board:
    def __init__(self, players: List[Player], width: int = 7, height: int = 6, win_condition: int = 4):
        self.grid: List[List[Optional[Player]]] = [[None for _ in range(width)] for _ in range(height)]

        self.players: List[Player] = players
        self.current_player_index: int = 0
        self.win_condition: int = win_condition
        self.state: BoardState = BoardState.running

    @property
    def width(self) -> int:
        return len(self.grid[0])

    @property
    def height(self) -> int:
        return len(self.grid)

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_index]

    def randomize_order(self) -> None:
        random.shuffle(self.players)

    def next_player(self) -> None:
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def get_height(self, column_index: int) -> int:
        return len([x for x in [row[column_index] for row in self.grid] if x is not None])

    def is_full(self, column_index: int) -> bool:
        return self.get_height(column_index) == self.height

    def place(self, column_index: int) -> None:
        if self.state != BoardState.running:
            return  # TODO: Erreur?
        if self.is_full(column_index):
            return  # TODO: Erreur
        row = self.get_height(column_index)
        self.grid[row][column_index] = self.current_player
        if self.check_win(row, column_index):
            self.state = BoardState.won
            return
        if all(self.is_full(index) for index in range(self.width)):
            self.state = BoardState.draw
        self.next_player()

    def get_player_at(self, row: int, col: int) -> Optional[Player]:
        return None if not (0 <= row < self.height and 0 <= col < self.width) else self.grid[row][col]

    def check_win(self, row: int, col: int) -> bool:
        player = self.get_player_at(row, col)
        if player is None:
            return False
        for direction in [(1, 0), (1, 1), (0, 1), (-1, 1)]:
            for i in range(self.win_condition):
                if len({self.get_player_at(row - (i - j) * direction[0],
                                           col - (i - j) * direction[1]) for j in range(self.win_condition)}) == 1:
                    return True
        return False

    def __str__(self) -> str:
        max_length = max([len(player.name) for player in self.players])
        rows = ["|".join(f"{'' if el is None else el.name:{max_length}}" for el in row) for row in self.grid]
        return f"\n{'|'.join(['-' * max_length for _ in range(self.width)])}\n".join(rows[::-1])
