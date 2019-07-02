import random, copy, math
from random import randint, shuffle
import time
import operator
from collections import defaultdict

class Elections:

	CANDIDATE_INDEX = 0
	CANDIDATE_RANK = NUMBER_OF_VOTES = CANDIDATE_SCORE = 1

	candidates = dict() # DICTIONARY OF KEY -> INDEX OF CANDIDATE, VALUE -> NUMBER OF VOTES
	voters = []	# LIST OF DICTIONAIRIES WICH HOLDS KEY -> INDEX CANDIDATE, VALUE -> RATING OF THE VOTER FOR THE CANDIDATE
	votes = dict() # DICTIONARY OF KEY -> INDEX OF CANDIDATE, VALUE -> SET WITH THE INDICES OF THE VOTERS THAT VOTED FOR THIS CANDIDATE
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

	leading_candidates = [] # INDICES OF CANDIDATES LEADING THE ELECTIONS: THE FIRST (N_VACANCIES + 1) CANDIDATES
	excluded = set() # SET UTILIZED IN IRV TO KEEP TRACK OF THE CANDIDATES EXCLUDED FROM THE ELECTIONS
	rounds = [] # LIST WITH THE RESULTS FOR EACH ROUND OF IRV

	def __init__(self, n_voters, bias_vector, n_vacancies, tactical = 0, minority = 0, tactical_votes = [], minority_votes = [], coalitions = [], candidates_names = [], voter_profiles = [], seed = 4):
		self.N_VOTERS = n_voters # NUMBER OF VOTERS
		self.N_CANDIDATES = len(bias_vector) # NUMBER OF CANDIDATES
		self.BIAS_VECTOR = bias_vector # INDICATES THE DISTRIBUTION USED FOR EACH CANDIDATE - VALUES FROM 0 TO 4: 0 (WORST CHANCE FOR GETTING GOOD RATING) , 4 (BEST CHANCE FOR GETTING GOOD RATINGS)
		self.N_VACANCIES = n_vacancies # NUMBER OF VACANCIES
		self.candidates_names = candidates_names # NAMES OF CANDIDATES
		self.TACTICAL_VOTING = tactical # BOOLEAN - ENABLES/DISABLES TACTICAL VOTING
		self.MINORITY_VOTING = minority # BOOLEAN - ENABLES/DISABLES MINORITY VOTING
		self.tactical_vote_percentages = tactical_votes # INDICATES THE PERCENTAGE OF TACTICAL VOTES RECEIVED FOR EACH CANDIDATE
		self.minority_vote_percentages = minority_votes # INDICATES THE PERCENTAGE OF MINORITY VOTES RECEIVED FOR EACH CANDIDATE
		self.coalitions = coalitions # LIST OF COALITIONS
		self.voter_profiles = voter_profiles # LIST OF VOTER'S PROFILES. EXAMPLE OF VOTER PORFILE: {"pop_percentage": 50, "scores": [10, 5, 4, 3, 2, 1, -10]}
		if seed is not None:
			random.seed(seed)

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

	# RESETS EVERY STRUCTURE
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
		# IN GENERATE MODE OF THE SIMULATOR VOTERS PREFERENCES ARE GENERATED FROM EACH CANDIDATE'S SET DISTRIBUTION
		if(not len(self.voter_profiles)):
			print("Generating Voters")
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
		# IN MANIPULATE MODE VOTER'S PREFERENCES ARE SET FROM VOTER'S PROFILES
		else:
			# print("Used Profiles")
			ranges = [] # LIST OF EACH PROFILE'S POPULATION PERCENTAGE
			ranks = [] # LIST OF EACH PROFILE'S RANKING OF CANDIDATES
			for prof in self.voter_profiles:
				# print(prof)
				ranges.append(int(prof["pop_percentage"]))
				rank = {}
				for index, score in enumerate(prof["scores"]):
					rank[index] = score
				ranks.append(rank)
			# print("RANGES::: ", ranges)
			# print("RANKS:::: ", ranks)
			for index, _range in enumerate(ranges):
				for _ in range(int(self.N_VOTERS*(_range/100))):
					self.voters.append(copy.deepcopy(ranks[index]))
		now = time.time()
		print('voters creation: ' + str(round(now - start_time, 2)) + ' seg' )

	# EVERY CANDIDATE IN A COALITION ADDS TO ITS SCORE HALF THE POINTS OF THE OTHER CANDIDATES IN THE COALITION
	def _account_for_coalitions(self):
		for voter_index, voter in enumerate(copy.deepcopy(self.voters)):
			for coalition in self.coalitions:
				for candidate in coalition:
					add_to_score = 0
					for candidate2 in coalition:
						if candidate == candidate2:
							continue
						add_to_score += math.floor(voter[candidate2['value']]/2)
					if self.voters[voter_index][candidate['value']] + add_to_score > 10:
						self.voters[voter_index][candidate['value']] = 10
					elif self.voters[voter_index][candidate['value']] + add_to_score < -10:
						self.voters[voter_index][candidate['value']] = -10
					else:
						self.voters[voter_index][candidate['value']] += add_to_score

	# SORT EACH VOTER'S CANDIDATE'S RANKING
	def sort_ranks(self):
		
		self._account_for_coalitions()

		start_time = time.time()
		# SORTING EACH VOTER'S RANKING OF CANDIDATES
		for voter in self.voters:
			self.sorted_voters.append(sorted(voter.items(), key=operator.itemgetter(1)))

		temp = []

		# THIS CREATES A DICT FOR EACH VOTER'S RANKING AND APPENDS TO 'temp' LIST. DICT WITH KEY => SOCORE AND VALUE => LIST WITH CANDIDATES WITH THAT SCORE
		for voter in self.sorted_voters:
			new_dict = defaultdict(list)
			for k in voter:
				new_dict[k[1]].append(k[0])
			temp.append(new_dict)

		self.sorted_voters = []

		# THIS PROCEDURE IS TO AVOID FAVORING CANDIDATES WITH HIGHER INDICES WHEN MULTIPLE CANDIDATES HAS THE SAME SCORE WITHIN A VOTER'S RANKING
		# THE DICTS IN 'temp' ARE TRANSFORMED BACK TO THE RANKINGS BUT WHEN THERE IS A LIST OF CANDIDATES WITH THE SAME SCORE THE LIST IS SHUFFLED 
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

		self.sorted_candidates = self.sort_candidates(self.candidates)
		self._set_leading_candidates()

	# THIS FILLS 'leading_candidates' LIST: THE FIRST (N_VACANCIES + 1) CANDIDATES
	def _set_leading_candidates(self):
		if self.N_VACANCIES == 1 or self.N_VACANCIES == 2:
			self.leading_candidates.append(self.sorted_candidates[-1][self.CANDIDATE_INDEX])
			self.leading_candidates.append(self.sorted_candidates[-2][self.CANDIDATE_INDEX])
			self.leading_candidates.append(self.sorted_candidates[-3][self.CANDIDATE_INDEX])
		elif self.N_VACANCIES > 2:
			for i in range(1, self.N_VACANCIES + 2):
				self.leading_candidates.append(self.sorted_candidates[-i][self.CANDIDATE_INDEX])
		
		print("leading: ", self.leading_candidates)		

	def sort_candidates(self, candidates):
			return sorted(candidates.items(), key=operator.itemgetter(1))

	# THIS METHOD CALCULATES BOTH THE MEAN OF THE SCORE OF THE WINNERS OF THE ELECTIONS AND THE PERCENTAGE OF THE VOTERS SATISFIED WITH THE RESULTS
	# THE MEAN IS THE SUM OF THE SCORES OF EACH CANDIDATE PER VOTER DIVIDED BY THE NUMBER OF VOTERS AND NUMBER OF VACANCIES
	# THE SATISFACTION RATE IS THE NUMBER OF VOTERS SATISFIED OVER THE TOTAL NUMBER OF VOTERS
	# A VOTER IS SATISFIED WHEN THE MEAN OF THE SCORES HE GAVE TO THE WINNERS IS POSITIVE (>0)
	def calculate_mean(self, winners):
		rating_sum = 0
		c = 0
		satisfied_population_count = 0
		for voter in self.voters:
			c += 1
			voter_satisfaction = 0
			for candidate in winners:
				rating_sum += voter[candidate]
				voter_satisfaction += voter[candidate]
			# print("::::VS: ", voter_satisfaction)
			if voter_satisfaction > 0:
				satisfied_population_count += 1
		print(":::rating sum: ", rating_sum)
		print(":::satisfied_pop_count: ", satisfied_population_count)
		print(":::N Voters: ", self.N_VOTERS)
		print(":::Count: ", c)
		print(":::Winners: ", winners)
		return rating_sum/(self.N_VOTERS*self.N_VACANCIES), satisfied_population_count/self.N_VOTERS