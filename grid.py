class Grid:
	def __init__(self, w, h, default=' '):
		self.cells = [
			[default for _ in range (w)]
			for _ in range(h)
		]
	
	def set(self, w, h, char):
		self.cells[h][w] = char
		
	def stripe_up(self, w, h, height, char='|'):
		for q in range(height):
			if h-q < 0: continue
			try:    self.cells[h-q][w] = char
			except: pass
	def write_at(self, w, h, string):
		for i, s in enumerate(string):
			try:    self.cells[h][w+i] = s
			except: pass
	
	def print_grid(self):
		for row in self.cells:
			print(''.join(row))