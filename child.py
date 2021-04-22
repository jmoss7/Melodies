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


	# ************* TEST ME!!!!!!!! ********************
	# change one random note in the melody (data attribute)
	# select random note:
	#	add/subtract MIDI number by random number from 1 to 11 to change note
	def mutate(self):
		if len(self.getData().getNotes()) == 0:
			print("ERROR: Could not mutate empty melody")
			exit(1)
		else:
			randNote = random.choice(self.getData().getNotes())
			print("old note: %d" % randNote.getMidiNumber())
			newMidi = randNote.getMidiNumber() + random.randint(-11, 12)
			# if note too high/low, add/subtract octave
			if newMidi < 12:
				newMidi += 12
			elif newMidi > 107:
				newMidi -= 12
			# set new MIDI number to note
			randNote.setMidiNumber(newMidi)
			print("new note: %d" % randNote.getMidiNumber())





	# For variation with genetic algorithm. Changes a random note within the Melody.
	#def mutate(self):






