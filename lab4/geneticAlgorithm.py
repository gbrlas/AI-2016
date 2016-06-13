import numpy as np
import random

class GeneticAlgorithm(object):
	"""
		Implement a simple generationl genetic algorithm as described in the instructions
	"""

	def __init__(	self, chromosomeShape,
					errorFunction,
					elitism = 1,
					populationSize = 25,
					mutationProbability  = .1,
					mutationScale = .5,
					numIterations = 10000,
					errorTreshold = 1e-6
					):

		self.populationSize = populationSize # size of the population of units
		self.p = mutationProbability # probability of mutation
		self.numIter = numIterations # maximum number of iterations
		self.e = errorTreshold # threshold of error while iterating
		self.f = errorFunction # the error function (reversely proportionl to fitness)
		self.keep = elitism  # number of units to keep for elitism
		self.k = mutationScale # scale of the gaussian noise

		self.i = 0 # iteration counter

		# initialize the population randomly from a gaussian distribution
		# with noise 0.1 and then sort the values and store them internally

		self.population = []
		for _ in range(populationSize):
			chromosome = np.random.randn(chromosomeShape) * 0.1

			fitness = self.calculateFitness(chromosome)
			self.population.append((chromosome, fitness))

		# sort descending according to fitness (larger is better)
		self.population = sorted(self.population, key=lambda t: -t[1])

	def step(self):
		"""
			Run one iteration of the genetic algorithm. In a single iteration,
			you should create a whole new population by first keeping the best
			units as defined by elitism, then iteratively select parents from
			the current population, apply crossover and then mutation.

			The step function should return, as a tuple:

			* boolean value indicating should the iteration stop (True if
				the learning process is finished, False otherwise)
			* an integer representing the current iteration of the
				algorithm
			* the weights of the best unit in the current iteration

		"""

		self.i += 1

		#############################
		#       YOUR CODE HERE      #
		#############################

		stop = False

		if self.numIter <= self.i:
			stop = True

		newPopulation = list()
		bestN = self.bestN(self.keep)

		for best in bestN:
			newPopulation.append(best)

		while len(newPopulation) < self.populationSize:
			p1, p2 = self.selectParents()
			d1 = self.crossover(p1,p2)

			d1 = self.mutate(d1)

			newPopulation.append((d1,self.calculateFitness(d1)))


		self.population = sorted(newPopulation,key = lambda t: -t[1])

		best_weights = self.best()

		return (stop, self.i, best_weights)


	def calculateFitness(self, chromosome):
		"""
			Implement a fitness metric as a function of the error of
			a unit. Remember - fitness is larger as the unit is better!
		"""
		chromosomeError = self.f(chromosome)

		#############################
		#       YOUR CODE HERE      #
		#############################
		return 1.0 / chromosomeError

	def bestN(self, n):
		"""
			Return the best n units from the population
		"""
		#############################
		#       YOUR CODE HERE      #
		#############################

		best = [x for x in self.population[0:n]]

		return best

	def best(self):
		"""
			Return the best unit from the population
		"""
		#############################
		#       YOUR CODE HERE      #
		#############################
		return self.population[0][0]


	def selectParents(self):
		"""
			Select two parents from the population with probability of
			selection proportional to the fitness of the units in the
			population
		"""
		#############################
		#       YOUR CODE HERE      #
		#############################
		parents = list()
		total_fitness = 0

		for unit in self.population:
			total_fitness += unit[1]

		while len(parents) < 2:
			for unit in self.population:
				if len(parents) >= 2:
					break

				if random.random() < unit[1] / total_fitness:
					parents.append(unit)

		return parents[0][0],parents[1][0]

	def crossover(self, p1, p2):
		"""
			Given two parent units p1 and p2, do a simple crossover by
			averaging their values in order to create a new child unit
		"""
		#############################
		#       YOUR CODE HERE      #
		#############################

		return np.add(p1,p2) / 2

	def mutate(self, chromosome):
		"""
			Given a unit, mutate its values by applying gaussian noise
			according to the parameter k
		"""

		#############################
		#       YOUR CODE HERE      #
		#############################

		#width of chromosome array
		for i in range(chromosome.shape[0]) :
			if random.random() <= self.p:
				chromosome[i] += random.gauss(0, self.k)

		return chromosome


