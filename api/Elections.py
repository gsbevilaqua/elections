import random
from random import randint, shuffle
import time
import operator
from collections import defaultdict

class Elections:

	CANDIDATE_INDEX = 0
	CANDIDATE_RANK = NUMBER_OF_VOTES = 1

	candidates = dict() # DICTIONARY OF KEY -> INDEX OF CANDIDATE, VALUE -> NUMBER OF VOTES
	voters = []	# LIST OF DICTIONAIRIES WICH HOLDS KEY -> INDEX CANDIDATE, VALUE -> RATING OF THE VOTER FOR THE CANDIDATE
	votes = dict()
	sorted_voters = [] # LIST OF VOTERS, EACH VOTER BEING A LIST OF TUPLES -> (INDEX OF CANDIDATE, RATING) IN ORDER FROM LOWER RANKED CANDIDATE TO HIGHEST RANKED
	sorted_candidates = [] # LIST OF CANDIDATES IN ORDER FROM LEAST VOTED TO MOST VOTED
	uniform = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0] # EQUAL CHANCE TO EACH RATING - UNIFORM
	neutral = [0.0, 0.01, 0.02, 0.04, 0.06, 0.09, 0.12, 0.16, 0.23, 0.34, 0.66, 0.77, 0.84, 0.88, 0.91, 0.94, 0.96, 0.98, 0.99, 1.0, 1.0] # HIGHER CHANCE FOR RATES CLOSE TO 0 - NEUTRAL
	liked = [0.0, 0.0, 0.01, 0.02, 0.03, 0.055, 0.08, 0.105, 0.13, 0.155, 0.18, 0.23, 0.28, 0.33, 0.39, 0.45, 0.54, 0.63, 0.745, 0.86, 1.0] # HIGH CHANCE OF GOOD RATING
	disliked = [0.14, 0.255, 0.37, 0.46, 0.55, 0.61, 0.67, 0.72, 0.77, 0.82, 0.845, 0.87, 0.895, 0.92, 0.945, 0.97, 0.98, 0.99, 1.0, 1.0, 1.0] # LOW CHANCE OF GOOD RATING
	loved = [0.0, 0.0, 0.0, 0.0, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.075, 0.125, 0.19, 0.255, 0.32, 0.4, 0.5, 0.6, 0.725, 0.85, 1.0] # HIGHEST CHANCE OF GOOD RATING
	hated = [0.15, 0.275, 0.4, 0.5, 0.6, 0.68, 0.745, 0.81, 0.875, 0.925, 0.95, 0.96, 0.97, 0.98, 0.99, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0] # LOWEST CHANCE OF GOOD RATING
	polarizer = [0.1, 0.19, 0.28, 0.35, 0.41, 0.436, 0.452, 0.468, 0.484, 0.5, 0.5, 0.516, 0.532, 0.548, 0.564, 0.59, 0.65, 0.72, 0.81, 0.9, 1.0] # HIGH CHANCE OF WORST RATINGS AND BEST RATINGS
	more_polarizer = [0.15, 0.25, 0.35, 0.4, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.5, 0.51, 0.52, 0.53, 0.54, 0.55, 0.6, 0.65, 0.75, 0.85, 1.0] # HIGHER CHANCE OF WORST RATINGS AND BEST RATINGS

	leading_candidates = []
	excluded = set()
	rounds = []

	def __init__(self, n_voters, bias_vector, n_vacancies,  tactical_votes, minority_votes, candidates_names = []):
		self.N_VOTERS = n_voters # NUMBER OF VOTERS
		self.N_CANDIDATES = len(bias_vector) # NUMBER OF CANDIDATES
		self.BIAS_VECTOR = bias_vector # VECTOR OF HELP VALUES FROM 0 TO 4 FOR CANDIDATES - 0 (WORST CHANCE FOR GETTING GOOD RATING) , 4 (BEST CHANCE FOR GETTING GOOD RATINGS)
		self.N_VACANCIES = n_vacancies
		self.candidates_names = candidates_names
		self.tactical_vote_percentages = tactical_votes
		self.minority_vote_percentages = minority_votes
		random.seed(4)

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
		self.leading_candidates = []

	def _sortear(self, dist):
		res = -10
		rand = random.random()
		for value in dist:
			if value > rand:
				return res
			else:
				res += 1

	# CREATES DICT OF CANDIDATES => (KEY: INDEX OF CANDIDATE, VALUE: NUMBER OF VOTES)
	def create_candidates(self):
		start_time = time.time()
		for i in range(self.N_CANDIDATES):
			self.candidates[i] = 0
			self.votes[i] = set()
		now = time.time()
		print('candidates creation: ' + str(round(now - start_time, 2)) + ' seg' )

	# CREATES LIST OF VOTERS (LIST OF DICTS) => [(KEY: INDEX OF CANDIDATE, VALUE: RATING), (), ...]
	def create_voters(self):
		start_time = time.time()
		for voter in range(self.N_VOTERS):
			candidates_rank = dict()
			for candidate in reversed(range(self.N_CANDIDATES)):
				if(self.BIAS_VECTOR[candidate]==4):
					candidates_rank[candidate] = self._sortear(self.loved)
				elif(self.BIAS_VECTOR[candidate]==3):
					candidates_rank[candidate] = self._sortear(self.liked)
				elif(self.BIAS_VECTOR[candidate]==2):
					candidates_rank[candidate] = self._sortear(self.disliked)								
				elif(self.BIAS_VECTOR[candidate]==1):
					candidates_rank[candidate] = self._sortear(self.hated)
				elif(self.BIAS_VECTOR[candidate]==-1):
					candidates_rank[candidate] = self._sortear(self.polarizer)
				elif(self.BIAS_VECTOR[candidate]==-2):
					candidates_rank[candidate] = self._sortear(self.more_polarizer)				
				else:
					candidates_rank[candidate] = self._sortear(self.neutral)
			self.voters.append(candidates_rank)
		now = time.time()
		print('voters creation: ' + str(round(now - start_time, 2)) + ' seg' )

	# SORT EACH VOTER'S CANDIDATE'S RANKING
	def sort_ranks(self):
		start_time = time.time()
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
			for rating, candidate_indexes in current_voter.items():
				if len(current_voter[rating]) > 1:
					shuffle(current_voter[rating])
					for e in candidate_indexes:
						new_voter.append((e, rating))
				else:
					new_voter.append((candidate_indexes[0], rating))
			self.sorted_voters.append(new_voter)
			self.candidates[new_voter[-1][0]] += 1
			self.votes[new_voter[-1][0]].add(voter_index)

		now = time.time()
		print('sorting: ' + str(round(now - start_time, 2)) + ' seg' )

	def sort_candidates(self, candidates):
			return sorted(candidates.items(), key=operator.itemgetter(1))

	def calculate_mean(self, winner):
		rating_sum = 0
		#c = 0
		satisfied_population_count = 0
		for voter in self.voters:
			#c += 1
			rating_sum += voter[winner]
			if voter[winner] > 0:
				satisfied_population_count += 1
		print(":::rating sum: ", rating_sum)
		print(":::N Voters: ", self.N_VOTERS)
		#print(":::Count: ", c)
		print(":::Winner: ", winner)
		return rating_sum/self.N_VOTERS, satisfied_population_count/self.N_VOTERS