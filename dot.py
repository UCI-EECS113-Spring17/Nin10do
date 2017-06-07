class Dot:
	
	x = 0
	y = 0
	occupied = 0
	
	def __init__(self, x ,y):
		self.x = x
		self.y = y
		self.occupied = 0
	
	def get_x(self):
		return self.x
	
	def get_y(self):
		return self.y
	
	def get_occupied(self):
		return self.occupied
		
	def set_occupied(self, x):
		self.occupied = x