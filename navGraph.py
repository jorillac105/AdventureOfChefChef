import edge
import node
import math
import queue as Q

class navGraph():
	def __init__(self, map, walkableTiles, levelNum):
		self.tiles = walkableTiles
		self.graph = self.createNodes(map)
		self.createEdges()

		self.levelNum = levelNum

		# for y in range(len(self.graph)):
		# 	for x in range(len(self.graph[y])):
		# 		if self.graph[y][x] is None:
		# 			print (" ")
		# 			print ("x = ", x, "y = ", y, " NONE")
		# 		else:
		# 			print ("Parent:")
		# 			print ("x = ", x, "y = ", y, " 1")
		# 			print ("Edges:")
		# 			for edge in self.graph[y][x].getEdges():
		# 				node = edge.getNextNode(self.graph[y][x])
		# 				xPos, yPos = node.getPos()
		# 				print ("x = ", xPos," y = ", yPos, " weight = ", edge.getWeight())
		# 	print (" ")

	def createNodes(self, map):
		graph = []
		for y in range(len(map)):
			xLine = []
			for x in range(len(map[y])):
				value = map[y][x]
				if value in self.tiles:
					n = self.createNode(x, y)
				else:
					n = None
				xLine.append(n)
			graph.append(xLine)
		return graph

	#creates 1 node
	def createNode(self, xPos, yPos):
		return node.Node(xPos, yPos)

	#creates edges for each node in the node graph
	def createEdges(self):
		#square root of 2
		#diagW = math.sqrt(2)
		diagW = 1.0
		#for each node in the graph
		for y in range(len(self.graph)):
			for x in range(len(self.graph[y])):
				#check if it exists
				if self.graph[y][x] is not None:
					node = self.graph[y][x]
					# check area below and to the right of node
					#CHECK NOT GOING AROUND CORNER
					if y < len(self.graph) - 1:
						# S
						if self.graph[y+1][x] is not None:
							self.addEdges(y+1, x, node, 1.0)
							#if there is not a corner in between here and SW,
							#ie, if south AND west are both walkable
							# SW
							if x > 0 and self.graph[y][x-1] is not None and self.graph[y+1][x-1] is not None:
								self.addEdges(y+1, x-1, node, diagW)
							#if there is not a corner in between here and SE,
							#ie, if south AND east are both walkable
							# SE
							if x < len(self.graph[y]) - 1 and self.graph[y][x+1] is not None and self.graph[y+1][x+1] is not None:
								self.addEdges(y+1, x+1, node, diagW)

					# E
					if x < len(self.graph[y]) - 1 and self.graph[y][x+1] is not None:
						self.addEdges(y, x+1, node, 1.0)

	#creates edges to and from 2 nodes with given weight
	def addEdges(self, yPos, xPos, fromNode, weight):
		#adds an edge from fromNode to the other node
		fromNode.addEdge(edge.Edge(self.graph[yPos][xPos], fromNode, weight))
		#adds an edge from the other node to fromNode
		self.graph[yPos][xPos].addEdge(edge.Edge(fromNode, self.graph[yPos][xPos], weight))

	def getNode(self, x, y):
		while y >= self.getHeight()//50:
			y -= 1
		while y < 0:
			y += 1
		while x >= self.getWidth()//50:
			x += 1
		while x < 0:
			x += 1
		return self.graph[y][x]

	def getWidth(self):
		return len(self.graph[0]) * 50

	def getHeight(self):
		return len(self.graph) * 50

	def getLevel(self):
		return self.levelNum


	def heuristic(self, goal, cur):
		goalX, goalY = goal.getPos()
		curX, curY = cur.getPos()
		dx = abs(curX - goalX)
		dy = abs(curY - goalY)
		return (dx + dy) + (math.sqrt(2) - 2) * min(dx, dy)

	def nodeExists(self, x, y):
		if y >= self.getHeight()//50 or x >= self.getWidth()//50 or x <= 0 or y <= 0:
			return False
		if self.graph[y][x] is None:
			return False
		return True

	#A* NAVIGATION, go to README to see inspiration
	def navigate(self, fromNode, toNode):
		frontier = Q.PriorityQueue()
		frontier.put((0, fromNode))
		cameFrom = { }
		costSoFar = { }
		cameFrom[fromNode] = None
		costSoFar[fromNode] = 0.0

		if toNode is None:
			print ("!ERROR! : ToNode does not exist")
		if fromNode is None:
			print ("!ERROR! : FromNode does not exist")


		while not frontier.empty(): 

			curTup = frontier.get()
			cur = curTup[1]

			if cur is toNode:
				break

			for edge in cur.getEdges():
				nextNode = edge.getNextNode(cur)
				newCost = costSoFar[cur] + edge.getWeight()

				if nextNode not in costSoFar or newCost < costSoFar[nextNode]:
					costSoFar[nextNode] = newCost
					priority = newCost + self.heuristic(toNode, nextNode)

					frontier.put((priority, nextNode))
					cameFrom[nextNode] = cur

		cur = toNode
		path = [cur]
		while cur in cameFrom and cur is not fromNode:
			cur = cameFrom[cur]
			path.append(cur)
		path.reverse()

		# print ("------------PATHING------------")
		# for node in path:
		# 	xPos, yPos = node.getPos()
		# 	print ("xPos = ",xPos," yPos = ",yPos)
		return path
