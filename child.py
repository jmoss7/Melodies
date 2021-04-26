from melody import Melody
from scales import *

import random


class Child:
	# initialize child in a population
	def __init__(self, data: Melody):
		self.data = data
		self.rating = None
		self.fitness = None
		self.chosen = False

	def getData(self):
		return self.data

	def getRating(self):
		return self.rating

	def getFitness(self):
		return self.fitness

	def isChosen(self):
		return self.chosen

	def setChosen(self):
		self.chosen = True

	def unsetChosen(self):
		self.chosen = False

	def setData(self, newData: Melody):
		self.data = newData

	def setRating(self, newRating):
		self.rating = newRating

	def setFitness(self, newfitness):
		self.fitness = newfitness






	# Creates a new Melody obj, placing it in a new Child obj
	# NOTE: does NOT copy rating or fitness
	def makeCopy(self):
		if self.getData() == None:
			print("makeCopy error: no data")
			exit(1)
		return Child(self.getData().duplicate())



	# Crosses two children using Melody.swapSegments()
	# NOTE: Should play around with swapPos in swapSegments() function
	def crossover(self, other):
		swapPos = random.randint(1, len(self.getData()))
		self.getData().swapSegments(other.getData(), swapPos)





	# For GenAlgo. Changes one random note in the melody (data attribute)
	# 1) Select random note in melody (self.data). Fail if empty melody
	# 2) Select random note (newNote) within scale of melody
	# 3) If randNote = -1, change a note to a rest, or rest to a note
	# 		Else, replace note with newNote
	# 4) Flag melody as modified
	def mutate(self):
		if len(self.getData().getNotes()) == 0:
			print("ERROR: Could not mutate empty melody")
			exit(1)
		else:
			mel = self.getData()
			scale = generate_scale(mel.getKeySignature(),
				mel.getScale(), mel.getOctave())

			randNote = random.choice(mel.getNotes())
			newNote = random.choice(scale)

			if randNote.getVelocity() == 0:
				randNote.setVelocity(64)
				randNote.setMidiNumber(random.choice(scale[:-1]))
			else:
				if newNote == -1:
					randNote.setVelocity(0)
				else:
					randNote.setMidiNumber(newNote)


			mel.setAsModified()


















