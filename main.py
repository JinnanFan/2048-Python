from game import Game
from tkinter import *

root = Tk()
root.configure(bg='black')
root.title("2048")

scoreBoard = Frame(root, bg='green', width=100, height=100)
scoreBoard.grid(row=0,column=0, columnspan=4)

gameBoard = Frame(root, bg='red', width=400, height=400)
gameBoard.grid(row=1,column=0)

game = Game(gameBoard, root)

root.bind("<Up>", game.up)
root.bind("<Down>", game.down)
root.bind("<Left>", game.left)
root.bind("<Right>", game.right)

root.mainloop()           