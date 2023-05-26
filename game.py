#!/usr/bin/env python
from tkinter import ttk
import random
import time
from settings import (
    GRID_SIZE,
    TILE_WIDTH,
    START_X,
    START_Y,
    TILE_DISTANCE,
    COLORS
)


class Game(ttk.Frame):
    def __init__(self, board, window):
        self.window = window
        self.board = board
        self.tileValues = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        # self.tileValues = [[2**(j+4*i) for j in range(1,GRID_SIZE+1)] for i in range(GRID_SIZE)]
        self.boardChanged = False
        self.score = 0
        self.gameOver = False
        self.start_game()

    def start_game(self):
        self.create_grid()
        self.add_new_tile()
        self.add_new_tile()
        self.update_tiles()

    def create_grid(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                self.create_tile(
                    START_X + TILE_DISTANCE * i, START_Y + TILE_DISTANCE * j
                )

    def create_tile(self, x, y, value=0):
        tileColor = COLORS[value] if int(value) <= 2048 else COLORS['other']
        tileText = value if value > 0 else None
        self.board.create_rectangle(
            (x, y),
            (x + TILE_WIDTH, y + TILE_WIDTH),
            fill=tileColor,
            outline=COLORS['text']
        )
        self.board.create_text(
            (x + TILE_WIDTH // 2, y + TILE_WIDTH // 2),
            anchor="center",
            font=("Clear Sans", 50-5*len(str(value)), 'bold'),
            fill=COLORS['text'],
            text=tileText,
        )

    def update_tiles(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.tileValues[i][j]>0:
                    self.create_tile(
                        START_X + TILE_DISTANCE * j,
                        START_Y + TILE_DISTANCE * i,
                        value=self.tileValues[i][j],
                    )

                else:
                    self.create_tile(
                        START_X + TILE_DISTANCE * j, START_Y + TILE_DISTANCE * i
                    )

    def update_score(self, score):
        self.score += score

    def game_over(self):
        if (
            not self.emptyCellAvailable()
            and not self.horizontalMoveAvailable()
            and not self.verticalMoveAvailable()
        ):
            self.gameOver = True

    def horizontalMoveAvailable(self):
        for i in range(3):
            for j in range(GRID_SIZE):
                if self.tileValues[i][j] == self.tileValues[i + 1][j]:
                    return True
        return False

    def verticalMoveAvailable(self):
        for i in range(GRID_SIZE):
            for j in range(3):
                if self.tileValues[i][j] == self.tileValues[i][j + 1]:
                    return True
        return False

    def add_new_tile(self):
        if self.emptyCellAvailable():
            while True:
                row = random.randint(0, 3)
                col = random.randint(0, 3)
                if self.tileValues[row][col] == 0:
                    break

            if random.randint(0, 9) == 0:
                self.tileValues[row][col] = 4
            else:
                self.tileValues[row][col] = 2

    def emptyCellAvailable(self):
        # for i in range(GRID_SIZE):
        #     for j in range(GRID_SIZE):
        #         if not self.tileValues[i][j]:
        #             return True
        # return False
        return any(0 in row for row in self.tileValues)

    # User interaction function for moving a tile
    def up(self, event):
        self.move_tile_up_and_merge()
        self.after_move()

    def left(self, event):
        self.transpose_left()
        self.move_tile_up_and_merge()
        self.transpose_left()
        self.after_move()

    def down(self, event):
        self.upside_down()
        self.move_tile_up_and_merge()
        self.upside_down()
        self.after_move()

    def right(self, event):
        self.transpose_left()
        self.upside_down()
        self.move_tile_up_and_merge()
        self.upside_down()
        self.transpose_left()
        self.after_move()

    def move_tile_up_and_merge(self):
        self.move_tile_up()
        self.merge_tile_up()
        self.move_tile_up()

    def move_tile_up(self):
        for i in range(1, GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.tileValues[i][j] > 0:
                    fillingPosition = i
                    while (
                        self.tileValues[fillingPosition - 1][j] == 0
                        and fillingPosition > 0
                    ):
                        fillingPosition -= 1
                    if fillingPosition != i:
                        self.tileValues[fillingPosition][j] = self.tileValues[i][j]
                        self.tileValues[i][j] = 0
                        self.boardChanged = True

    def merge_tile_up(self):
        score = 0
        for i in range(GRID_SIZE-1):
            for j in range(GRID_SIZE):
                if (
                    self.tileValues[i][j] > 0
                    and self.tileValues[i][j] == self.tileValues[i + 1][j]
                ):
                    self.tileValues[i][j] *= 2
                    self.tileValues[i + 1][j] = 0
                    self.boardChanged = True

                    score += self.tileValues[i][j]

        self.update_score(score)

    def transpose_left(self):
        for i in range(GRID_SIZE):
            for j in range(i, GRID_SIZE):
                self.tileValues[i][j], self.tileValues[j][i] = (
                    self.tileValues[j][i],
                    self.tileValues[i][j],
                )

    def upside_down(self):
        for i in range(GRID_SIZE//2):
            for j in range(GRID_SIZE):
                self.tileValues[i][j], self.tileValues[3 - i][j] = (
                    self.tileValues[3 - i][j],
                    self.tileValues[i][j],
                )

    def after_move(self):
        if self.boardChanged:
            self.add_new_tile()

        self.update_tiles()
        self.game_over()
        self.boardChanged = False

    def __repr__(self):
        return self.tileValues
