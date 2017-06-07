class Map:
	
	width = 0
	height = 0
	max_lvl = 0
	detail = None
	
	def __init__(self):
		self.width = 16
		self.height = 12
		self.max_lvl = 3
		self.detail = [[[0 for col in range(self.width)]for row in range(self.height)] for x in range(self.max_lvl)]
		self.detail[0] = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
					 [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
					 [1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1],
					 [1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1],
					 [1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1],
					 [1,3,0,0,1,1,1,1,1,1,1,1,1,1,1,1],
					 [1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1],
					 [1,2,0,0,1,1,1,1,1,1,1,1,1,1,1,1],
					 [1,0,4,0,0,1,1,1,1,1,1,1,1,1,1,1],
					 [1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1],
					 [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
					 [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
		
		self.detail[1] = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
					 [1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1],
					 [1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1],
					 [1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1],
					 [1,1,1,1,1,1,2,3,1,1,0,0,0,0,0,1],
					 [1,1,1,1,1,0,0,1,1,1,0,2,0,1,1,1],
					 [1,1,1,1,1,2,0,0,4,0,0,0,0,1,1,1],
					 [1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
					 [1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1],
					 [1,1,1,1,1,1,3,0,1,1,1,1,0,1,1,1],
					 [1,1,1,1,1,1,1,1,1,1,1,1,3,1,1,1],
					 [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
					 
		self.detail[2] = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
					 [1,1,1,1,1,1,1,3,0,0,0,1,0,1,1,1],
					 [1,1,1,0,0,0,0,0,1,0,0,1,0,1,1,1],
					 [1,1,1,0,1,0,1,0,0,0,1,0,0,1,1,1],
					 [1,1,1,0,3,0,0,1,0,0,1,0,0,1,1,1],
					 [1,1,1,0,1,0,0,1,2,1,1,2,0,1,1,1],
					 [1,1,1,0,0,0,1,0,0,0,0,0,0,1,1,1],
					 [1,1,1,1,0,0,1,0,4,0,0,0,1,1,1,1],
					 [1,1,1,0,0,1,1,0,0,0,1,1,1,1,1,1],
					 [1,1,1,0,0,0,2,0,0,0,0,3,0,1,1,1],
					 [1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1],
					 [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
					 
	def get_lvl(self, x):
		return self.detial[x]
	
	def get_max_lvl(self):
		return self.max_lvl