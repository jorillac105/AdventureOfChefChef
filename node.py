class Node():
	def __init__(self, xPos, yPos):
		self.xPos = xPos
		self.yPos = yPos
		self.edges = []

	def __lt__(self, other):
		return other

	def setPos(self, xPos, yPos):
		self.xPos = xPos
		self.yPos = yPos

	def addEdge(self, newEdge):
		self.edges.append(newEdge)

	def getPos(self):
		return self.xPos, self.yPos

	def getEdges(self):
		return self.edges