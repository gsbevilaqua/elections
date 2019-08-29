import random, copy, math, time
from api.Elections import Elections
#from Elections import Elections # used for testing

class FirstPastThePost:

	elec = None # ELECTIONS OBJECT
	candidates = dict() # DICTIONARY OF KEY -> INDEX OF CANDIDATE, VALUE -> NUMBER OF VOTES
	sorted_candidates = [] # LIST OF CANDIDATES IN ORDER FROM LEAST VOTED TO MOST VOTED
	votes = dict() # DICTIONARY OF KEY -> INDEX OF CANDIDATE, VALUE -> SET WITH THE INDICES OF THE VOTERS THAT VOTED FOR THIS CANDIDATE
	votes_copy = dict() # COPY OF VOTES DICT
	t_votes_changed = 0 # NUMBER OF VOTES CHANGED BEACAUSE OF TACTICAL VOTING
	m_votes_changed = 0 # NUMBER OF VOTES CHANGED BEACAUSE OF MINORITY VOTING
	rankings_changed = dict()

	# STRUCTURES NEEDS TO BE COPIED TO BE MODIFIED WITHOUT AFFECTING THE SIMULATION OF OTHER ELECTION METHODS
	def __init__(self, elec):
		start_time = time.time()
		self.elec = elec
		self.candidates = copy.deepcopy(elec.candidates)
		self.votes = copy.deepcopy(elec.votes)
		self.votes_copy = copy.deepcopy(elec.votes)
		self.sorted_candidates = elec.sorted_candidates
		if elec.seed is not None:
			random.seed(elec.seed)
		print('FPTP init: ' + str(round(time.time() - start_time, 2)) + ' seg' )

	def reset(self):
		self.t_votes_changed = 0
		self.m_votes_changed = 0
		self.rankings_changed = dict()

	# CANDIDATES THAT ARE NOT IN 'leading_candidates' LIST LOSE VOTES TO LEADING CANDIDATES BASED ON LEADING CANDIDATES TACTICAL VOTING PERCENTAGE PARAMETER
	def _count_tactical_votes(self):
		print("::::::::COUNTING TACTICAL VOTES...")
		self.t_votes_changed = 0
		for candidate in self.votes_copy:
			if candidate not in self.elec.leading_candidates:
				for voter_index in self.votes_copy[candidate]:
					for index, _candidate in enumerate(reversed(self.elec.sorted_voters[voter_index])):
						if _candidate[self.elec.CANDIDATE_INDEX] in self.elec.leading_candidates:
							if random.random() < self.elec.tactical_vote_percentages[_candidate[self.elec.CANDIDATE_INDEX]]:
								# print(candidate)
								# print(self.elec.sorted_voters[voter_index])
								# print(_candidate[self.elec.CANDIDATE_INDEX])
								# print("index: ", -(index + 1))
								self.t_votes_changed += 1
								self.rankings_changed[voter_index] = copy.deepcopy(self.elec.sorted_voters[voter_index])
								# print(self.rankings_changed[voter_index][-(index + 1)])
								self.rankings_changed[voter_index][-(index + 1)], self.rankings_changed[voter_index][-1] = self.rankings_changed[voter_index][-1], self.rankings_changed[voter_index][-(index + 1)]
								self.candidates[candidate] -= 1
								self.candidates[_candidate[self.elec.CANDIDATE_INDEX]] += 1
								self.votes[candidate].remove(voter_index)
								self.votes[_candidate[self.elec.CANDIDATE_INDEX]].add(voter_index)
								# print(self.rankings_changed[voter_index])
								break
							break # without this break a voter could change its vote to a candidate in leading_cadidates that is not his actual preference between them
		print(":::::T votes changed: ", self.t_votes_changed)

	# CANDIDATES THAT ARE NOT IN 'leading_candidates' LIST GAIN VOTES FROM LEADING CANDIDATES BASED IN ITS MINORITY VOTING PERCENTAGE PARAMETER					
	def _count_minority_votes(self):
		print("::::::::COUNTING MINORITY VOTES...")
		self.m_votes_changed = 0
		half_vacancies = math.floor(self.elec.N_VACANCIES/2)

		for candidate in self.elec.leading_candidates:
			if self.elec.leading_candidates.index(candidate) >= half_vacancies:
				continue
			for voter_index in self.votes_copy[candidate]:
				if voter_index in self.rankings_changed:
					ranking = self.rankings_changed[voter_index]
				else:
					ranking = copy.deepcopy(self.elec.sorted_voters[voter_index])
				for index, _candidate in enumerate(reversed(ranking)):
					if _candidate[self.elec.CANDIDATE_INDEX] not in self.elec.leading_candidates or (_candidate[self.elec.CANDIDATE_INDEX] in self.elec.leading_candidates and self.elec.leading_candidates.index(_candidate[self.elec.CANDIDATE_INDEX]) >= half_vacancies):
						if _candidate[self.elec.CANDIDATE_RANK] >= 0:
							if random.random() < self.elec.minority_vote_percentages[_candidate[self.elec.CANDIDATE_INDEX]]:
								self.m_votes_changed += 1
								self.candidates[candidate] -= 1
								self.candidates[_candidate[self.elec.CANDIDATE_INDEX]] += 1
								break
							break
						break
			
		print(":::::M votes changed: ", self.m_votes_changed)

	def simulate(self):
		print("FIRST PAST THE POST")
		start_time = time.time()

		if self.elec.N_CANDIDATES > 3 and self.elec.TACTICAL_VOTING:
			self._count_tactical_votes()
		if self.elec.N_VACANCIES > 1 and self.elec.MINORITY_VOTING:
			self._count_minority_votes()
		self.sorted_candidates = self.elec.sort_candidates(self.candidates)

		out = [[], []]
		for candidate in self.sorted_candidates:
			out[0].append(self.elec.candidates_names[candidate[self.elec.CANDIDATE_INDEX]])
			out[1].append(candidate[self.elec.CANDIDATE_SCORE])

		winners = []
		vacancies = self.elec.N_VACANCIES
		for candidate in reversed(self.sorted_candidates):
			if vacancies == 0:
				break
			winners.append(candidate[0])
			vacancies -= 1
		mean, satisfaction_rate, chose_best = self.elec.get_mean(winners = winners)

		elected = out[0][-self.elec.N_VACANCIES:]

		now = time.time()
		print('FPTP duration: ' + str(round(now - start_time, 2)) + ' seg' )
		return out, mean, elected, satisfaction_rate, chose_best