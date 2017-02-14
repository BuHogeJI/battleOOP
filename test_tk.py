class Sea:
	
	def makeSea(self):
		self.sea = Canvas(root, width = 1000, height = 500, bg = 'black', cursor = 'plus')
		self.sea.bind('<Button-1>', self.move)

	def setPlayers(self):
		board = Board(10, 10)
		player = Player('Player1', 10, 10)
		player.setBoard()
		player.setEnemyBoard()
		player.setRandShip()
		computer = Player('Computer', 10, 10)
		computer.setBoard()
		computer.setRandShip()
		return player, computer

	def getPlayers(self):
		self.player, self.computer = self.setPlayers()

	def makeBoard(self):
		y = 30
		for row in self.player.board:
			x = 30
			for col in row:
				if col == u'\u00B7': self.sea.create_rectangle(x, y, x + 30, y + 30, fill = 'white', tag = '{}-{}'.format(x // 30 - 1, y // 30 - 1))
				else: self.sea.create_rectangle(x, y, x + 30, y + 30, fill = 'lightgreen', tag = '{}-{}'.format(x // 30 - 1, y // 30 - 1))
				x += 30
			y += 30

	def makeEnemyBoard(self):
		y = 30
		for row in self.player.enemy_board:
			x = 500
			for col in row:
				self.sea.create_rectangle(x, y, x + 30, y + 30, fill = 'white', tag = '{}-{}'.format(x // 30 - 1, y // 30 - 1))
				x += 30
			y += 30

	def move(self, event):
		first_coord = event.x
		second_coord = event.y
		y = 30
		for row in self.computer.board:
			x = 500
			for col in row:
				if first_coord > x and first_coord < x + 30: first_coord = x
				if second_coord > y and second_coord < y + 30: second_coord = y
				x += 30
			y += 30
		first_coord = first_coord // 30 - 1
		second_coord = second_coord // 30 - 1
		print(first_coord, second_coord)
		if self.computer.board[second_coord][first_coord - 15] == u'\u00B7': color = 'pink'
		else:
			for i, ship in enumerate(self.computer.ships):
				if [second_coord, first_coord - 15] in ship:
					self.player.killed_ships.append([second_coord, first_coord - 15])
					ship.remove([second_coord, first_coord - 15])
				if len(ship) == 0:
					for move in self.player.killed_ships[i]:
						pass
						
			color = 'red' 
			self.sea.itemconfig('{}-{}'.format(first_coord + 1, second_coord - 1), fill = 'pink')
			self.sea.itemconfig('{}-{}'.format(first_coord - 1, second_coord + 1), fill = 'pink')
			self.sea.itemconfig('{}-{}'.format(first_coord + 1, second_coord + 1), fill = 'pink')
			self.sea.itemconfig('{}-{}'.format(first_coord - 1, second_coord - 1), fill = 'pink')
		self.sea.itemconfig('{}-{}'.format(first_coord, second_coord), fill = color)

		

	

if __name__ == '__main__':
	from tkinter import *
	import string
	from battleOOP2 import *

	root = Tk()
	canv = Sea()
	canv.makeSea()
	canv.getPlayers()
	canv.makeBoard()
	canv.makeEnemyBoard()
	canv.sea.pack()
	root.mainloop()