from abc import ABC, abstractmethod

class Entity(ABC):
	def __init__(self):
		super(Entity, self).__init__()


	@abstractmethod
	def getXPos():
		pass

	@abstractmethod
	def getYPos():
		pass

	@abstractmethod
	def getHeight():
		pass

	@abstractmethod
	def getCameraPos():
		pass