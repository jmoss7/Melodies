from child import Child
from typing import List


class Generation:

	def __init__(self, children: List[Child], gen: int):

		if not children:
			self.children = []
		else:
			self.children = children

		self.gen = gen
		self.totalFitness = None
	

	def __str__(self):
		if len(self.children) == 0:
			return "No children in this gen"
		else:
			return "Gen {}".format(self.getGen())

	def __repr__(self):
		return str(self)

	def getChildren(self):
		return self.children

	def getGen(self):
		return self.gen

	def getTotalFitness(self):
		return self.totalFitness

	# Find the total fitness value to calculate selection probabilities for next generation
	def calculateTotalFitness(self):
		total = 0
		for c in self.children:
			total += c.getFitness()
		self.totalFitness = total

	# Normalize fitness value of each individual so that sum of all values equals 1:
	def normalizeFitness(self):
		for c in self.getChildren():
			curFit = c.getFitness()
			print("%d / %d: " % (curFit, self.totalFitness))
			normalized = curFit / float(self.totalFitness)
			print(normalized)
			c.setFitness(normalized)















