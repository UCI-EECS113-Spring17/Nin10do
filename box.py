class Box:
	
	x = 0
	y = 0
	can_move = 0
	
	def __init__(self, x ,y):
		self.x = x
		self.y = y
		self.can_move = 1
	
	def get_x(self):
		return self.x
	
	def get_y(self):
		return self.y
		
	def set_x(self, x):
		self.x = x
	
	def set_y(self, y):
		self.y = y
		
	def get_can_move(self):
		return self.can_move
		
	def set_can_move(self, x):
		self.can_move = x