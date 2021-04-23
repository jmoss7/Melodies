from melody import Melody

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
	# 2) Generate random number from -11 to 12
	# 3) If rng = 0, change a note to a rest, or rest to a note
	# 		Else, add/subtract MIDI number by rng
	# 4) Flag melody as modified
	def mutate(self):
		if len(self.getData().getNotes()) == 0:
			print("ERROR: Could not mutate empty melody")
			exit(1)
		else:
			randNote = random.choice(self.getData().getNotes())
			rng = random.randint(-11, 12)
			print("RNG NUMBER IS %d" % rng)
			if rng == 0:
				if randNote.getVelocity() == 0:
					randNote.setVelocity(64)
				else:
					randNote.setVelocity(0)
			else:
				newMidi = randNote.getMidiNumber() + rng
				if newMidi < 12:
					newMidi += 12
				elif newMidi > 107:
					newMidi -= 12
				randNote.setMidiNumber(newMidi)
			self.getData().setAsModified()


















