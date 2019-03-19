import random
from random import randint, shuffle
import time
import operator

class Elections:

	N_VACANCIES = 1 # NUMBER OF VACANCIES (NOT IMPLEMENTED YET)
	CANDIDATE_INDEX = 0
	CANDIDATE_RANK = NUMBER_OF_VOTES = 1

	candidates = dict() # DICTIONARY OF KEY -> INDEX OF CANDIDATE, VALUE -> NUMBER OF VOTES
	voters = []	# LIST OF DICTIONAIRIES WICH HOLDS KEY -> INDEX CANDIDATE, VALUE -> RATING OF THE VOTER FOR THE CANDIDATE
	votes = dict()
	sorted_voters = [] # LIST OF VOTERS, EACH VOTER BEING A LIST OF TUPLES -> (INDEX OF CANDIDATE, RATING) IN ORDER FROM LOWER RANKED CANDIDATE TO HIGHEST RANKED
	sorted_candidates = [] # LIST OF CANDIDATES IN ORDER FROM LEAST VOTED TO MOST VOTED
	neutral = [(-10,1), (-9,2), (-8,3), (-7,4), (-6,5), (-5,6), (-4,7), (-3,8), (-2,9), (-1,10), (0,11), (1,12), (2,13), (3,14), (4,15), (5,16), (6,17), (7,18), (8,19), (9,20), (10,21)] # EQUAL CHANCE TO EACH RATING - NEUTRAL
	lucky = [(-10,1), (-9,2), (-8,3), (-7,4), (-6,5), (-5,6), (-4,7), (-3,8), (-2,9), (-1,10), (0,11), (1,12), (2,13), (3,14), (4,15), (5,17), (6,19), (7,21), (8,23), (9,25), (10,27)] # HIGH CHANCE OF GOOD RATING
	unlucky = [(-10,2), (-9,4), (-8,6), (-7,8), (-6,10), (-5,12), (-4,13), (-3,14), (-2,15), (-1,16), (0,17), (1,18), (2,19), (3,20), (4,21), (5,22), (6,23), (7,24), (8,25), (9,26), (10,27)] # LOW CHANCE OF GOOD RATING
	really_lucky = [(-10,1), (-9,2), (-8,3), (-7,4), (-6,5), (-5,6), (-4,7), (-3,8), (-2,9), (-1,10), (0,12), (1,14), (2,16), (3,18), (4,20), (5,23), (6,26), (7,29), (8,32), (9,35), (10,38)] # HIGHEST CHANCE OF GOOD RATING
	really_unlucky = [(-10,3), (-9,6), (-8,9), (-7,12), (-6,15), (-5,18), (-4,20), (-3,22), (-2,24), (-1,26), (0,28), (1,29), (2,30), (3,31), (4,32), (5,33), (6,34), (7,35), (8,36), (9,37), (10,38)] # LOWEST CHANCE OF GOOD RATING
	polarizer = [(-10,3), (-9,6), (-8,9), (-7,12), (-6,13), (-5,14), (-4,15), (-3,16), (-2,17), (-1,18), (0,19), (1,20), (2,21), (3,22), (4,23), (5,24), (6,25), (7,28), (8,31), (9,34), (10,37)] # HIGH CHANCE OF WORST RATINGS AND BEST RATINGS
	more_polarizer = [(-10,5), (-9,10), (-8,15), (-7,20), (-6,21), (-5,22), (-4,23), (-3,24), (-2,25), (-1,26), (0,27), (1,28), (2,29), (3,30), (4,31), (5,32), (6,33), (7,38), (8,43), (9,48), (10,53)] # HIGHER CHANCE OF WORST RATINGS AND BEST RATINGS

	excluded = set()
	rounds = []

	def __init__(self, n_voters, n_candidates, bias_vector):
		self.N_VOTERS = n_voters # NUMBER OF VOTERS
		self.N_CANDIDATES = n_candidates # NUMBER OF CANDIDATES
		self.BIAS_VECTOR = bias_vector # VECTOR OF HELP VALUES FROM 0 TO 4 FOR CANDIDATES - 0 (WORST CHANCE FOR GETTING GOOD RATING) , 4 (BEST CHANCE FOR GETTING GOOD RATINGS)

	def initialize(self):
		start_time = time.time()
		self.create_candidates()
		now = time.time()
		print('candidates creation: ' + str(round(now - start_time, 2)) + ' seg' )
		self.create_voters()
		now = time.time()
		print('voters creation: ' + str(round(now - start_time, 2)) + ' seg' )
		self.sort_ranks()
		now = time.time()
		print('sorting: ' + str(round(now - start_time, 2)) + ' seg' )

	def reset(self):
		self.excluded = set()
		self.rounds = []
		self.winner = -1
		self.second_place = -1
		self.candidates = dict()
		self.voters = []
		self.votes = dict()
		self.sorted_voters = []
		self.sorted_candidates = []	

	def sortear(self, values_and_accumulated_frequencie, accumulated_value):
	    x = randint(0, accumulated_value-1)
	    for value, accumulated_value in values_and_accumulated_frequencie:
	        if x < accumulated_value:
	            return value

	# CREATES DICT OF CANDIDATES => (KEY: INDEX OF CANDIDATE, VALUE: NUMBER OF VOTES)
	def create_candidates(self):
		for i in range(self.N_CANDIDATES):
			self.candidates[i] = 0
			self.votes[i] = []

	# CREATES LIST OF VOTERS (LIST OF DICTS) => [(KEY: INDEX OF CANDIDATE, VALUE: RATING), (), ...]
	def create_voters(self):
		for voter in range(self.N_VOTERS):
			candidates_rank = dict()
			for candidate in range(self.N_CANDIDATES):
				if(self.BIAS_VECTOR[candidate]==4):
					candidates_rank[candidate] = self.sortear(self.really_lucky, 38)
				elif(self.BIAS_VECTOR[candidate]==3):
					candidates_rank[candidate] = self.sortear(self.lucky, 27)
				elif(self.BIAS_VECTOR[candidate]==2):
					candidates_rank[candidate] = self.sortear(self.unlucky, 27)								
				elif(self.BIAS_VECTOR[candidate]==1):
					candidates_rank[candidate] = self.sortear(self.really_unlucky, 38)
				elif(self.BIAS_VECTOR[candidate]==-1):
					candidates_rank[candidate] = self.sortear(self.polarizer, 37)
				elif(self.BIAS_VECTOR[candidate]==-2):
					candidates_rank[candidate] = self.sortear(self.more_polarizer, 53)				
				else:
					candidates_rank[candidate] = self.sortear(self.neutral, 21)

			self.voters.append(candidates_rank)

	# SORT EACH VOTER'S CANDIDATE'S RANKING
	def sort_ranks(self):
		for voter in self.voters:
			self.sorted_voters.append(sorted(voter.items(), key=operator.itemgetter(1)))

		for voter_index, voter in enumerate(self.sorted_voters):
			new_order = []
			for candidate in range(self.N_CANDIDATES - 1):
				if voter[self.N_CANDIDATES - 1 - candidate][self.CANDIDATE_RANK] == voter[self.N_CANDIDATES - 2 - candidate][self.CANDIDATE_RANK]:
					new_order.append(voter[self.N_CANDIDATES - 1 - candidate])
					if candidate == self.N_CANDIDATES - 2:
						new_order.append(voter[self.N_CANDIDATES - 2 - candidate])
						shuffle(new_order)
						self.sorted_voters[voter_index] = new_order
						self.candidates[self.sorted_voters[voter_index][-1][self.CANDIDATE_INDEX]] += 1
						self.votes[self.sorted_voters[voter_index][-1][self.CANDIDATE_INDEX]].append(voter_index)
						break
					continue
				else:
					if(candidate == 0):
						self.candidates[self.sorted_voters[voter_index][-1][self.CANDIDATE_INDEX]] += 1
						self.votes[self.sorted_voters[voter_index][-1][self.CANDIDATE_INDEX]].append(voter_index)
						break
					else:
						new_order.append(voter[self.N_CANDIDATES - 1 - candidate])
						shuffle(new_order)
						for _ in range(candidate + 1):
							self.sorted_voters[voter_index].pop(-1)
						self.sorted_voters[voter_index].extend(new_order)
						self.candidates[self.sorted_voters[voter_index][-1][self.CANDIDATE_INDEX]] += 1
						self.votes[self.sorted_voters[voter_index][-1][self.CANDIDATE_INDEX]].append(voter_index)
						break

	def sort_candidates(self, candidates):
			return sorted(candidates.items(), key=operator.itemgetter(1))