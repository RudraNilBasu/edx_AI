class Node:

	def __key(self):
		string = '['.join('['.join('%s' %x for x in y) for y in self.state)
		hashcode = string.replace("[","")
		return hashcode

	def __init__(self, state, parent, direction, depth, cost):
		self.state = state
		self.parent = parent
		self.depth = depth
		self.cost = cost
		self.direction = direction

	def __lt__(self, other):
		return self.cost <= other.cost