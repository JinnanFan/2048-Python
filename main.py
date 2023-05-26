import tkinter as tk

from game import Game
from settings import GRID_WIDTH,COLORS

root = tk.Tk()
root.configure(bg='black')
root.title("2048")

# scoreBoard = tk.Frame(root, bg='green', width=100, height=100)
# scoreBoard.pack()

gameCanvas = tk.Canvas(root, bg=COLORS[0], width=GRID_WIDTH, height=GRID_WIDTH)
gameCanvas.pack(anchor="center", expand=True)

game = Game(gameCanvas, root)

root.bind("<Up>", game.up)
root.bind("<Down>", game.down)
root.bind("<Left>", game.left)
root.bind("<Right>", game.right)

root.mainloop()           