#!/usr/bin/env python
from tkinter import *
from tkinter import ttk
import random



class Game(ttk.Frame):
    def __init__(self):
        ttk.Frame.__init__(self)
        self.grid()
        self.master.title('2048')
        # self.master.geometry('410x510')

        self.start_game()

        self.master.bind('<Up>', self.up)
        self.master.bind('<Down>', self.down)
        self.master.bind('<Left>', self.left)
        self.master.bind('<Right>', self.right)


        self.style = ttk.Style(self)
        self.style.configure('gridFrame.TFrame',relief='sunken', background='green')
        self.style.configure('cellFrame.TFrame', background='red', relief='raised')
        # self.style.configure('cellNumber.TFrame', background='black', relief='raised', borderwidth=10)
        # self.infoBoard = ttk.Frame(self.master).grid(row=0)
        self.quit_game()



    def make_grid(self):
        self.gameBoard = ttk.Frame(self, style='gridFrame.TFrame', borderwidth=5)
        self.gameBoard.grid(row=2, columnspan=4)
        self.gridNumber = [[None for _ in range(4)] for _ in range(4)]
        self.grid = []
        

        for i in range(4):
            row = []
            for j in range(4): 
                # todo - hwo to bind cellLabel with cellFrame
                cellFrame = ttk.Frame(self.gameBoard, style='cellFrame.TFrame', width=100, height=100)
                cellFrame.grid(row=i, column=j, padx=5, pady=5)
                cellLabel = ttk.Label(self.gameBoard, font=("Helvetica", 18))
                cellLabel.grid(row=i, column=j)
                row.append({"frame": cellFrame, "label": cellLabel})
            self.grid.append(row)

        print(self.gridNumber)
        print(self.grid)
                

    def start_game(self):
        self.make_grid()

        self.score = 0
        scoreLF = ttk.LabelFrame(self, text="SCORE:")
        scoreLF.grid(row=0, column=3)
        self.scoreLabel = ttk.Label(scoreLF, text=self.score,  font=("Helvetica", 18))
        self.scoreLabel.grid()


        self.add_new_tile()
        self.add_new_tile()
        self.update_gridLabel()
 
    

    def update_score(self, score):
        self.score += score
        self.scoreLabel.configure(text=self.score)
        

    

    def game_over(self):
        if not self.emptyCellAvailable() and not self.horizontalMoveAvailable() and not self.verticalMoveAvailable():
            self.scoreLabel.configure(text="over")


    def horizontalMoveAvailable(self):
        for i in range(3):
            for j in range(4):
                if self.gridNumber[i][j] == self.gridNumber[i+1][j]:
                    return True
        return False

    def verticalMoveAvailable(self):
        for i in range(4):
            for j in range(3):
                if self.gridNumber[i][j] == self.gridNumber[i][j+1]:
                    return True
        return False
        

    def add_new_tile(self):
        if self.emptyCellAvailable():
            while True:
                row = random.randint(0,3)
                col = random.randint(0,3)
                if not self.gridNumber[row][col]:
                    break

            # new tile is 2 with possibility of 0.9 and 4 with possibility of 0.1
            if random.randint(0,9) == 0:
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

    def update_gridLabel(self):
        for i in range(4):
            for j in range(4):
                if self.gridNumber[i][j]:
                    self.grid[i][j]["label"].configure(text=self.gridNumber[i][j])
                else:
                    self.grid[i][j]["label"].configure(text='')

    


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
                    while not self.gridNumber[k-1][j] and k > 0:
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
                self.gridNumber[i][j], self.gridNumber[j][i] = self.gridNumber[j][i], self.gridNumber[i][j]
                   
        print("transpose_left: ", self.gridNumber)

    def upside_down(self):
        for i in range(2):
            for j in range(4):
                self.gridNumber[i][j], self.gridNumber[3-i][j] = self.gridNumber[3-i][j], self.gridNumber[i][j]


    def merge_tile_up(self):
        score = 0
        for i in range(3):
            for j in range(4):
                if self.gridNumber[i][j] and self.gridNumber[i][j] == self.gridNumber[i+1][j]:
                    self.gridNumber[i][j] *= 2
                    self.gridNumber[i+1][j] = None
                    score += self.gridNumber[i][j]

        self.update_score(score)
        print("merge up: ", self.gridNumber )
     
       




    def quit_game(self):
        quitButton = ttk.Button(self, text = 'Quit', command=quit)
        quitButton.grid(row=0, column=0)

        # self.quitKey = ttk.
        self.master.bind('<KeyPress-q>', quit)


def main():
    game2048 = Game()
    game2048.mainloop()


if __name__ == "__main__":
    main()