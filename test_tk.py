class Sea:
	
	def makeSea(self):
		self.sea = Canvas(root, width = 1000, height = 500, bg = 'black', cursor = 'plus')
		self.sea.bind('<Button-1>', self.move)

	def makeBoard(self):
		y = 30
		j = 0
		while j < 10:
			x = 0
			while x < 300:
				self.sea.create_rectangle(x, y, x + 30, y + 30, fill = 'white', tag = '{}-{}'.format(x, y))
				x += 30
			y += 30
			j += 1

	def makeShips(self):
		pass

	def move(self, event):
		firts_coord = event.x
		second_coord = event.y
		y = 30
		j = 0
		while j < 10:
			x = 0
			while x < 300:
				if firts_coord > x and firts_coord < x + 30: firts_coord = x
				if second_coord > y and second_coord < y + 30: second_coord = y
				x += 30
			y += 30
			j+= 1
		MISS = 'pink'
		self.sea.itemconfig('{}-{}'.format(firts_coord, second_coord), fill = MISS)
		

	

if __name__ == '__main__':
	from tkinter import *
	import string

	root = Tk()
	canv = Sea()
	canv.makeSea()
	canv.makeBoard()
	canv.sea.pack()
	root.mainloop()