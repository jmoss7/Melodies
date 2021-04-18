from melody import Melody


class Child:
	# initialize child in a population
	def __init__(self, data: Melody):
		self.data = data
		self.fitness = None
		self.probability = None

	def getData(self):
		return self.data

	def getFitness(self):
		return self.fitness

	def getProbability(self):
		return self.probability

	def setData(self, newData: Melody):
		self.data = newData

	def setFitness(self, newfitness):
		self.fitness = newfitness

	def setProbability(self, newProb: float):
		self.probability = newProb




