class Map:
	
	width = 16
	height = 12
	max_lvl = 1
	current_lvl = 0
	detail = None
	
	def __init__(self):
		self.width = 16
		self.height = 12
		self.max_lvl = 1
		self.current_lvl = 0
		self.detail = [[[0 for col in range(self.width)]for row in range(self.height)] for x in range(self.max_lvl)]
		self.detail[0] = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
					 [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
					 [1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1],
					 [1,3,0,0,1,1,1,1,1,1,1,1,1,1,1,1],
					 [1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1],
					 [1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1],
					 [1,0,0,0,0,0,0,0,4,1,1,1,1,1,1,1],
					 [1,2,0,0,1,1,1,1,1,1,1,1,1,1,1,1],
					 [1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1],
					 [1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1],
					 [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
					 [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
					 
	def get_lvl(self, x):
		return self.detial[x]