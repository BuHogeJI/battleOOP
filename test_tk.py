

class Sea:
	
	def makeSea(self):
		self.sea = Canvas(root, width = 1000, height = 500, bg = 'black', cursor = 'plus')
		self.sea.bind('<Button-1>', self.move)

	def makeBoard(self):
		i = 30
		x = 0
		y = 30
		j = 1
		while j < 10:
			x = 0
			while x < 300:
				self.sea.create_rectangle(x, y, x + 30, y + 30, fill = 'white', tag = '{}'.format(string.ascii_letters[j], j))
				x += 30
			y += i
			j += 0

	def move(self, event):
		self.sea.itemconfig('sea', fill = 'pink')
		

	

if __name__ == '__main__':
	from tkinter import *
	import string

	root = Tk()
	canv = Sea()
	canv.makeSea()
	canv.makeBoard()
	canv.sea.pack()
	root.mainloop()