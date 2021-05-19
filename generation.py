from child import Child
from typing import List

from play import *
from melodygen import *
from melodystack import MelodyStack
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.button import Button

import random
from numpy.random import choice


class Generation:

	def __init__(self, children: List[Child], gen: int):

		if not children:
			self.children = []
		else:
			self.children = children

		self.gen = gen
		self.totalRating = None
		self.isNormalized = False
		self.isSorted = False
		self.topRatingIdx = None # index of highest-rated melody
		self.probabilities = [] # selection probs (corresponds w/ children)
	

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

	def getTotalRating(self):
		return self.totalRating

	def getTopRatingIdx(self):
		return self.topRatingIdx

	def getProbabilities(self):
		return self.probabilities



    # Creates first generation
    # ******** self.children MUST BE EMPTY LIST *********
    # 1) Pick random instrument
    # 2) create 10 children with randomized melody from that same instrument
    # 3) append each child to self.children
	def createFirstGenWith10(self, scale, octave, key, bars):
		print("Creating first generation...")
		randInstr = chooseRandomInstrument(INSTRUMENT_NP_NS_WITHOUT_CATEGORY)
		for i in range(10):
			m = createMelody(instrument=randInstr, bpm=100, scale=scale, octave=octave, key_sig=key, bars=bars)
			self.children.append(Child(m))


	# Finds total fitness value of all ratings in generation
	def calculateTotalRating(self):
		total = 0
		for c in self.children:
			total += c.getRating()
		self.totalRating = total

	# Normalize fitness value of each individual
	# 	divide each individual rating by total rating
	# 	sum of all values should equal 1
	#	add to probabilities array (should correspond w/ children!)
	#	
	# error if no total rating
	def normalizeFitness(self):
		if self.getTotalRating() is None:
			print("ERROR: No total rating")
			exit(1)
		elif self.getTotalRating() == 0:
			print("ERROR: total rating is 0")
			exit(1)
		for c in self.getChildren():
			curFit = c.getRating()
			normalized = curFit / float(self.getTotalRating())
			c.setFitness(normalized)
			self.probabilities.append(normalized)
		self.isNormalized = True


	# Not using atm
	# Sort children in generation by fitness
	def sortChildrenByFitness(self):
		self.children.sort(key=lambda x: x.getFitness(), reverse=False)
		self.isSorted = True



	# finds and sets topRatingIdx (must all be rated first!!!!)
	def findHighest(self):
		highest_idx = 0
		highest_rating = 0
		curIdx = 0
		for child in self.getChildren():
			curRating = child.getRating()
			if curRating >= highest_rating:
				highest_rating = curRating
				highest_idx = curIdx
			curIdx += 1
		self.topRatingIdx = highest_idx


	# Assign ratings (fitness) to each child in the current generation
	# For each melody in generation:
	#	1) Plays current melody, saving over the old 'out.mid' and 'temp.wav'
	#   2) Asks for user to give 1-10 rating.
	#	3) Saves index of highest-rated melody to self.topRatingIdx
	#	4) Sets rating attribute of current child
	# NOTE: Should check if rating given is not 'r', 'replay', or 1-10 int
	def giveRatings(self):
		print("Rate each melody from 1 to 10.")
		count = 0
		highestRating = 0
		for child in self.getChildren():
			count += 1
			m = child.getData()
			m.generateMIDI()
			m.saveMelodyAs('out.mid')
			print("Playing Melody %d..." % count)
			midiToWAV("out.mid", "temp.wav")
			playWAVkivy("temp.wav")
			curOption = input("Rate this melody 1-10 or type 'r' or 'replay' to replay: ")
			while (curOption == "replay" or curOption == "r"):
				print("Replaying melody %d ..." % count)
				playWAVkivy("temp.wav")
				curOption = input("Rate this melody 1-10 or type 'replay' to replay: ")
			curRating = float(int(curOption))
			if curRating > highestRating:
				highestRating = curRating
				self.topRatingIdx = count - 1
			child.setRating(curRating)




#   SELECTION: Use numpy.random.choice() to select weighted individuals
#   Returns: pair of individuals [parent1, parent2]
	def selection(self):
		return choice(self.getChildren(), size=2,
			replace=False, p=self.getProbabilities())



	# NOT USING
	# select child with the highest fitness score
	# must be sorted AND have at least 2 children
	# returns new Child by copying top melody using Melody.duplicate() 
	def copyTopChild(self):
		if not self.isSorted:
			print("ERROR: NOT SORTED")
			exit(1)
		elif len(self.getChildren()) < 2:
			print("ERROR: THERE ARE %d CHILDREN" % len(self.getChildren()))
			exit(1)
		else:
			return Child(self.getChildren()[-1].getData().duplicate())


	# NOT IN USE, using advanceToNextGenWith10 instead
	# advance to next gen with 5 new children:
	#	selection:
	#		1) select top rated melody and create new child from it + mutate
	#		2) select 2 parents, make copies and crossover + mutate
	#		3) select 2 parents again, make copies and crossover + mutate
	#		4) mutate (change one random note) every child in next gen
	#		5) replace current generation with the 5 individuals above,
	#		6) restore all attributes (except children and gen) to default
	#	NOTE: should play around with what to pass to next gen:
	#		(choose 2 parents to crossover 2 times + top child) <- using this
	#		choose 2 parents to crossover 2 times + random child
	#		choose 2 parents to crossover once + top two + random child
	#		etc
	#	NOTE 2: try with 10?
	def advanceToNextGen(self):
		nextGen = []

		topIndividual = self.children[self.getTopRatingIdx()].makeCopy()
		topIndividual.mutate()
		nextGen.append(topIndividual)

		parents = self.selection()
		crossMe1 = parents[0].makeCopy()
		crossMe2 = parents[1].makeCopy()
		crossMe1.crossover(crossMe2)
		crossMe1.mutate()
		crossMe2.mutate()
		nextGen.append(crossMe1)
		nextGen.append(crossMe2)

		parents = self.selection()
		crossMe3 = parents[0].makeCopy()
		crossMe4 = parents[1].makeCopy()
		crossMe3.crossover(crossMe4)
		crossMe3.mutate()
		crossMe4.mutate()
		nextGen.append(crossMe3)
		nextGen.append(crossMe4)

		random.shuffle(nextGen)
		self.children = nextGen
		self.gen = self.gen + 1
		self.totalRating = None
		self.isNormalized = False
		self.isSorted = False
		self.topRatingIdx = None
		self.probabilities = []


#	USING THIS RIGHT NOW instead of with 5 
#	Same as advanceToNextGen except with 10 individuals per generation.
#	Chooses 10 parents, crosses and passes 9 children
#	Still chooses top individual
	def advanceToNextGenWith10(self):
		nextGen = []

		topIndividual = self.children[self.getTopRatingIdx()].makeCopy()
		topIndividual.mutate()
		nextGen.append(topIndividual)

		parents = self.selection()
		crossMe1 = parents[0].makeCopy()
		crossMe2 = parents[1].makeCopy()
		crossMe1.crossover(crossMe2)
		crossMe1.mutate()
		crossMe2.mutate()
		nextGen.append(crossMe1)
		nextGen.append(crossMe2)

		parents = self.selection()
		crossMe3 = parents[0].makeCopy()
		crossMe4 = parents[1].makeCopy()
		crossMe3.crossover(crossMe4)
		crossMe3.mutate()
		crossMe4.mutate()
		nextGen.append(crossMe3)
		nextGen.append(crossMe4)

		parents = self.selection()
		crossMe5 = parents[0].makeCopy()
		crossMe6 = parents[1].makeCopy()
		crossMe5.crossover(crossMe6)
		crossMe5.mutate()
		crossMe6.mutate()
		nextGen.append(crossMe5)
		nextGen.append(crossMe6)

		parents = self.selection()
		crossMe7 = parents[0].makeCopy()
		crossMe8 = parents[1].makeCopy()
		crossMe7.crossover(crossMe8)
		crossMe7.mutate()
		crossMe8.mutate()
		nextGen.append(crossMe7)
		nextGen.append(crossMe8)

		parents = self.selection()
		crossMe9 = parents[0].makeCopy()
		crossMe10 = parents[1].makeCopy()
		crossMe9.crossover(crossMe10)
		crossMe9.mutate()
		crossMe10.mutate()
		nextGen.append(random.choice((crossMe9, crossMe10)))

		random.shuffle(nextGen)
		self.children = nextGen
		self.gen = self.gen + 1
		self.totalRating = None
		self.isNormalized = False
		self.isSorted = False
		self.topRatingIdx = None
		self.probabilities = []






"""

	# NOT USING
	# for testing rating / sort function
	def printAllRatings(self):
		print("************** PRINTING RATINGS ******************")
		count = 0
		for child in self.getChildren():
			count += 1
			print("Rating: %d: %d" % (count, child.getRating()))


	# NOT USING
	# for testing fitness / sort function
	def printAllFitness(self):
		print("****** PRINTING FITNESS *********")
		count = 0
		for child in self.getChildren():
			count += 1
			print("Rating %d: %d" % (count, child.getRating()))
			print("Fitness %d: %f" % (count, child.getFitness()))
"""














