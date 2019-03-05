class Edge():
	def __init__(self, fromNode, toNode, weight):
		self.fromNode = fromNode
		self.toNode = toNode
		self.weight = weight

	def getNextNode(self, fromhere):
		if self.fromNode is fromhere:
			return self.toNode
		else:
			return self.fromNode

	def getWeight(self):
		return self.weight