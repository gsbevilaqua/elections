import random
from random import randint, shuffle
import time
import operator
from collections import defaultdict

class Elections:

	N_VACANCIES = 1 # NUMBER OF VACANCIES (NOT IMPLEMENTED YET)
	CANDIDATE_INDEX = 0
	CANDIDATE_RANK = NUMBER_OF_VOTES = 1

	candidates = dict() # DICTIONARY OF KEY -> INDEX OF CANDIDATE, VALUE -> NUMBER OF VOTES
	voters = []	# LIST OF DICTIONAIRIES WICH HOLDS KEY -> INDEX CANDIDATE, VALUE -> RATING OF THE VOTER FOR THE CANDIDATE
	votes = dict()
	sorted_voters = [] # LIST OF VOTERS, EACH VOTER BEING A LIST OF TUPLES -> (INDEX OF CANDIDATE, RATING) IN ORDER FROM LOWER RANKED CANDIDATE TO HIGHEST RANKED
	sorted_candidates = [] # LIST OF CANDIDATES IN ORDER FROM LEAST VOTED TO MOST VOTED
	neutral = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000] # EQUAL CHANCE TO EACH RATING - NEUTRAL
	lucky = [20, 50, 80, 110, 140, 180, 220, 260, 300, 340, 390, 440, 490, 540, 590, 640, 690, 750, 820, 900, 1000] # HIGH CHANCE OF GOOD RATING
	unlucky = [100, 180, 250, 310, 360, 410, 460, 510, 560, 610, 660, 700, 740, 780, 820, 860, 890, 920, 950, 980, 1000] # LOW CHANCE OF GOOD RATING
	really_lucky = [25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 325, 375, 425, 475, 525, 600, 675, 775, 875, 1000] # HIGHEST CHANCE OF GOOD RATING
	really_unlucky = [125, 225, 325, 400, 475, 425, 575, 625, 675, 725, 750, 775, 800, 825, 850, 875, 900, 925, 950, 975, 1000] # LOWEST CHANCE OF GOOD RATING
	polarizer = [(-10,3), (-9,6), (-8,9), (-7,12), (-6,13), (-5,14), (-4,15), (-3,16), (-2,17), (-1,18), (0,19), (1,20), (2,21), (3,22), (4,23), (5,24), (6,25), (7,28), (8,31), (9,34), (10,37)] # HIGH CHANCE OF WORST RATINGS AND BEST RATINGS
	more_polarizer = [(-10,5), (-9,10), (-8,15), (-7,20), (-6,21), (-5,22), (-4,23), (-3,24), (-2,25), (-1,26), (0,27), (1,28), (2,29), (3,30), (4,31), (5,32), (6,33), (7,38), (8,43), (9,48), (10,53)] # HIGHER CHANCE OF WORST RATINGS AND BEST RATINGS

	excluded = set()
	rounds = []

	def __init__(self, n_voters, bias_vector):
		print(random.random())
		self.N_VOTERS = n_voters # NUMBER OF VOTERS
		self.N_CANDIDATES = len(bias_vector) # NUMBER OF CANDIDATES
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

	def sortear(self, dist):
		res = -10
		rand = random.randrange(0, 1000)
		for value in dist:
			if value > rand:
				return res
			else:
				res += 1

	# CREATES DICT OF CANDIDATES => (KEY: INDEX OF CANDIDATE, VALUE: NUMBER OF VOTES)
	def create_candidates(self):
		for i in range(self.N_CANDIDATES):
			self.candidates[i] = 0
			self.votes[i] = []

	# CREATES LIST OF VOTERS (LIST OF DICTS) => [(KEY: INDEX OF CANDIDATE, VALUE: RATING), (), ...]
	def create_voters(self):
		for voter in range(self.N_VOTERS):
			candidates_rank = dict()
			for candidate in reversed(range(self.N_CANDIDATES)):
				if(self.BIAS_VECTOR[candidate]==4):
					candidates_rank[candidate] = self.sortear(self.really_lucky)
				elif(self.BIAS_VECTOR[candidate]==3):
					candidates_rank[candidate] = self.sortear(self.lucky)
				elif(self.BIAS_VECTOR[candidate]==2):
					candidates_rank[candidate] = self.sortear(self.unlucky)								
				elif(self.BIAS_VECTOR[candidate]==1):
					candidates_rank[candidate] = self.sortear(self.really_unlucky)
				elif(self.BIAS_VECTOR[candidate]==-1):
					candidates_rank[candidate] = self.sortear(self.polarizer)
				elif(self.BIAS_VECTOR[candidate]==-2):
					candidates_rank[candidate] = self.sortear(self.more_polarizer)				
				else:
					candidates_rank[candidate] = self.sortear(self.neutral)
			self.voters.append(candidates_rank)

	# SORT EACH VOTER'S CANDIDATE'S RANKING
	def sort_ranks(self):
		for voter in self.voters:
			self.sorted_voters.append(sorted(voter.items(), key=operator.itemgetter(1)))

		temp = []

		for voter in self.sorted_voters:
			new_dict = defaultdict(list)
			for k in voter:
				new_dict[k[1]].append(k[0])
			temp.append(new_dict)

		self.sorted_voters = []

		for voter_index, current_voter in enumerate(temp):
			new_voter = []
			for k, j in current_voter.items():
				if len(current_voter[k]) > 1:
					shuffle(current_voter[k])
					for e in j:
						new_voter.append((e, k))
				else:
					new_voter.append((j[0], k))
			self.sorted_voters.append(new_voter)
			self.candidates[new_voter[-1][0]] += 1
			self.votes[new_voter[-1][0]].append(voter_index)

		# for voter_index, voter in enumerate(self.sorted_voters):
		# 	new_order = []
		# 	for candidate in range(self.N_CANDIDATES - 1):
		# 		if voter[self.N_CANDIDATES - 1 - candidate][self.CANDIDATE_RANK] == voter[self.N_CANDIDATES - 2 - candidate][self.CANDIDATE_RANK]:
		# 			new_order.append(voter[self.N_CANDIDATES - 1 - candidate])
		# 			if candidate == self.N_CANDIDATES - 2:
		# 				new_order.append(voter[self.N_CANDIDATES - 2 - candidate])
		# 				shuffle(new_order)
		# 				self.sorted_voters[voter_index] = new_order
		# 				self.candidates[self.sorted_voters[voter_index][-1][self.CANDIDATE_INDEX]] += 1
		# 				self.votes[self.sorted_voters[voter_index][-1][self.CANDIDATE_INDEX]].append(voter_index)
		# 				break
		# 			continue
		# 		else:
		# 			if(candidate == 0):
		# 				self.candidates[self.sorted_voters[voter_index][-1][self.CANDIDATE_INDEX]] += 1
		# 				self.votes[self.sorted_voters[voter_index][-1][self.CANDIDATE_INDEX]].append(voter_index)
		# 				break
		# 			else:
		# 				new_order.append(voter[self.N_CANDIDATES - 1 - candidate])
		# 				shuffle(new_order)
		# 				for _ in range(candidate + 1):
		# 					self.sorted_voters[voter_index].pop(-1)
		# 				self.sorted_voters[voter_index].extend(new_order)
		# 				self.candidates[self.sorted_voters[voter_index][-1][self.CANDIDATE_INDEX]] += 1
		# 				self.votes[self.sorted_voters[voter_index][-1][self.CANDIDATE_INDEX]].append(voter_index)
		# 				break

	def sort_candidates(self, candidates):
			return sorted(candidates.items(), key=operator.itemgetter(1))