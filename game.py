#!/usr/bin/env python
from tkinter import Frame, Label
import random
import time


class Game:
    def __init__(self, gameFrame, window):
        self.window = window
        self.gameFrame = gameFrame
        self.gameOver = False
        self.score = 0
        self.create_grid(gameFrame)
        self.start_game()

    def start_game(self):
        self.add_new_tile()
        self.add_new_tile()
        self.update_gridLabel()

    def create_grid(self, gameFrame):
        self.oldGridNumber = [[None for _ in range(4)] for _ in range(4)]
        self.gridNumber = [[None for _ in range(4)] for _ in range(4)]
        self.grid = []

        for i in range(4):
            row = []
            for j in range(4):
                cellFrame = Frame(gameFrame, width=100, height=100)
                cellFrame.grid(row=i, column=j, padx=5, pady=5)
                cellLabel = Label(gameFrame, fg="orange", font=("Helvetica", 18))
                cellLabel.grid(row=i, column=j)
                row.append({"frame": cellFrame, "label": cellLabel})
            self.grid.append(row)

        print(self.gridNumber)

    def update_gridLabel(self):
        for i in range(4):
            for j in range(4):
                if self.gridNumber[i][j]:
                    self.grid[i][j]["label"].configure(text=self.gridNumber[i][j])

 
                else:
                    self.grid[i][j]["label"].configure(text="")
        self.animate_labels()

        # print('old', oldGridNumber)

    def animate_labels(self):
        for i in range(4):
            for j in range(4):
                if self.oldGridNumber[i][j] != self.gridNumber[i][j]:
                    print('--------------------------')
                    
                    self.grid[i][j]["label"].configure(fg = 'blue')
                    self.oldGridNumber[i][j] = self.gridNumber[i][j]
        self.gameFrame.update()
        time.sleep(0.5)
        
        for i in range(4):
            for j in range(4):
                self.grid[i][j]["label"].configure(fg = 'orange')

        

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
            for j in range(4):
                if self.gridNumber[i][j] == self.gridNumber[i + 1][j]:
                    return True
        return False

    def verticalMoveAvailable(self):
        for i in range(4):
            for j in range(3):
                if self.gridNumber[i][j] == self.gridNumber[i][j + 1]:
                    return True
        return False

    def add_new_tile(self):
        if self.emptyCellAvailable():
            while True:
                row = random.randint(0, 3)
                col = random.randint(0, 3)
                if not self.gridNumber[row][col]:
                    break

            if random.randint(0, 9) == 0:
                self.gridNumber[row][col] = 4
            else:
                self.gridNumber[row][col] = 2

            print("add new tile: ", self.gridNumber)

    def emptyCellAvailable(self):
        for i in range(4):
            for j in range(4):
                if not self.gridNumber[i][j]:
                    return True
        return False

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

    def after_move(self):
        self.add_new_tile()
        self.update_gridLabel()
        self.game_over()

    def move_tile_up(self):
        for i in range(1, 4):
            for j in range(4):
                if self.gridNumber[i][j]:
                    k = i
                    while self.gridNumber[k - 1][j] is None and k > 0:
                        k -= 1
                    if k != i:
                        self.gridNumber[k][j] = self.gridNumber[i][j]
                        self.gridNumber[i][j] = None

        print("move up: ", self.gridNumber)

    def move_tile_up_and_merge(self):
        self.move_tile_up()
        self.merge_tile_up()
        self.move_tile_up()

    def transpose_left(self):
        for i in range(4):
            for j in range(i, 4):
                self.gridNumber[i][j], self.gridNumber[j][i] = (
                    self.gridNumber[j][i],
                    self.gridNumber[i][j],
                )

        print("transpose_left: ", self.gridNumber)

    def upside_down(self):
        for i in range(2):
            for j in range(4):
                self.gridNumber[i][j], self.gridNumber[3 - i][j] = (
                    self.gridNumber[3 - i][j],
                    self.gridNumber[i][j],
                )

    def merge_tile_up(self):
        score = 0
        for i in range(3):
            for j in range(4):
                if (
                    self.gridNumber[i][j]
                    and self.gridNumber[i][j] == self.gridNumber[i + 1][j]
                ):
                    self.gridNumber[i][j] *= 2
                    self.gridNumber[i + 1][j] = None
                    score += self.gridNumber[i][j]

        self.update_score(score)
        print("merge up: ", self.gridNumber)

    def __repr__(self):
        return self.gridNumber
