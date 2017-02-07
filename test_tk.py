from tkinter import *

class Sea():

	def makeBoard(self):
		self.board = Frame(root)
		for r in range(10):
			for c in range(10):
				self.button = Button(self.board, bg = 'white', width = 6, height = 2)
				self.button.bind('<Button-1>', self.miss)
				self.button.grid(row  = r, column = c)
		self.board.grid(row = 0, column = 0)
		f = Frame(root, width = 100).grid(row = 0, column = 1)

	def makeEnemyBoard(self):
		self.enemy_board = Frame(root)
		for r in range(10):
			for c in range(10):
				self.button = Button(self.enemy_board, bg = 'white', width = 6, height = 2)
				self.button.bind('<Button-1>', self.miss)
				self.button.grid(row  = r, column = c)
		self.enemy_board.grid(row = 0, column = 2)

	def miss(self, event):
		self.button['bg'] = 'lightblue'

if __name__ == '__main__':
	root = Tk()
	sea = Sea()
	sea.makeBoard()
	sea.makeEnemyBoard()
	root.mainloop()