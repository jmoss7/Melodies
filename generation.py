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

	# Finds total fitness value of ratings
	def calculateTotalRating(self):
		total = 0
		for c in self.children:
			total += c.getRating()
		self.totalRating = total

	# Normalize fitness value of each individual
	# 	divide each individual rating by total rating
	# 	sum of all values should equals 1
	#	sort by fitness value
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
		self.sortChildrenByFitness()
		self.isNormalized = True

	# Sort children in generation by fitness
	def sortChildrenByFitness(self):
		self.children.sort(key=lambda x: x.getFitness(), reverse=False)
		self.isSorted = True


	# Assign ratings (fitness) to each child in the current generation
	def giveRatings(self):
		print("Rate each melody from 1 to 5:")
		count = 0
		for child in self.getChildren():
			count += 1
			m = child.getData()
			m.generateMIDI()
			m.saveMelodyAs('out.mid')
			print("Playing Melody %d..." % count)
			midiToWAV("out.mid", "temp.wav")
			playWAVkivy("temp.wav")
			curOption = input("Rate this melody 1-10 or type 'replay' to replay: ")
			while (curOption == "replay" or curOption == "Replay"):
				print("Replaying melody...")
				playWAVkivy("temp.wav")
				curOption = input("Rate this melody 1-10 or type 'replay' to replay: ")
			# ********** NEED ERROR CHECKING HERE *************
			# if option is not int from 1-10, error
			# else set rating of current melody
			curRating = float(int(curOption))
			child.setRating(curRating)


	# Selection process:
	#	random number R between 0 and 1 is chosen
	#	accumulated value = sum of fitness value + all previous fitness value
	#	the selected child is the first whose accumulated value >= R
	#	returns first chosen Child object and pops it from self.children
	# FITNESS MUST BE NORMALIZED TO WORK!!!!
	def selection(self):
		if self.isNormalized == False:
			print("ERROR: NOT NORMALIZED")
			exit(1)

		else:
			selected = None
			accum = 0
			r = random.random()
			print("current R: %f " % r)
			for i in range(len(self.getChildren())):
				# if selected, pop from list and re-normalize children
				accum = self.getChildren()[i].getFitness() + accum
				print("current accum: %f" % accum)
				if accum >= r:
					selected = self.children.pop(i)
					self.calculateTotalRating()
					self.normalizeFitness()
					return selected
#				if child.isChosen() == False and child.getFitness() >= r:
#					child.setChosen()
#					return child
			# should not get here. should always pick one
			print("ERROR: NONE CHOSEN")
			exit(1)


	# NOT CURRENTLY IN USE
	# select child with the highest fitness score
	# must be sorted AND have exactly 5 children !!
	def selectTopChild(self):
		if not self.isSorted:
			print("ERROR: NOT SORTED")
			exit(1)
		elif len(self.getChildren()) == 0:
			print("ERROR: THERE ARE %d CHILDREN" % len(self.getChildren()))
			exit(1)
		else:
			return self.children.pop()

	# NOT CURRENTLY IN USE
	# same as selectTopChild() but chooses second best instead of first
	def selectSecondBest(self):
		if not self.isSorted:
			print("ERROR: NOT SORTED")
			exit(1)
		elif len(self.getChildren()) == 0:
			print("ERROR: THERE ARE %d CHILDREN" % len(self.getChildren()))
			exit(1)
		else:
			return self.getChildren().pop(-2)


	# advance to next gen:
	#	selection: select parents and random survivor for next gen
	#	crossover: cross parents and pass children to next gen
	#	mutation: change random note in every child
	#def nextGen():


















	# for testing rating / sort function
	def printAllRatings(self):
		print("************** PRINTING RATINGS ******************")
		count = 0
		for child in self.getChildren():
			count += 1
			print("Rating: %d: %d" % (count, child.getRating()))


	# for testing fitness / sort function
	def printAllFitness(self):
		print("****** PRINTING FITNESS *********")
		count = 0
		for child in self.getChildren():
			count += 1
			print("Rating %d: %d" % (count, child.getRating()))
			print("Fitness %d: %f" % (count, child.getFitness()))

























