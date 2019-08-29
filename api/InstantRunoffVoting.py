import copy, time, random
from api.Elections import Elections
#from Elections import Elections # used for testing

class InstantRunoffVoting(Elections):	

	elec = None # ELECTIONS OBJECT
	candidates = dict() # DICTIONARY OF KEY -> INDEX OF CANDIDATE, VALUE -> NUMBER OF VOTES
	sorted_candidates = [] # LIST OF CANDIDATES IN ORDER FROM LEAST VOTED TO MOST VOTED
	votes = dict() # DICTIONARY OF KEY -> INDEX OF CANDIDATE, VALUE -> SET WITH THE INDICES OF THE VOTERS THAT VOTED FOR THIS CANDIDATE
	votes_copy = dict()
	leading_candidates = []
	rankings_changed = dict()

	def __init__(self, elec):
		start_time = time.time()
		self.elec = elec
		self.candidates = copy.deepcopy(elec.candidates)
		self.votes = copy.deepcopy(elec.votes)
		self.votes_copy = copy.deepcopy(elec.votes)
		print('IRV init: ' + str(round(time.time() - start_time, 2)) + ' seg' )

	def reset(self):
		self.leading_candidates = []
		self.sorted_candidates = []
		self.rankings_changed = dict()

	# FOR EVERY ROUND THIS METHOD IS CALLED. FOR EACH ROUND OF IRV VOTES OF ELIMINATED CANDIDATES ARE REDISTRIBUTED.
	# EXCLUDED ARRAY KEEPS TRACK OF THE ELIMINATED CANDIDATES. THE 3 IFS BELOW ARE FOR WHEN THE TWO LAST CANDIDATES
	# TIE WITH 50%/50%, FOR WHEN ONE CANDIDATE HAS REACHED MORE THAN 50% VOTES AND FOR WHEN NO CANDIDATE REACHED
	# MORE THAN 50% AND THE NEXT ROUND IS REQUIRED
	def _count_votes(self, _round):
		self.elec.rounds.append(self.sorted_candidates[_round:])
		if(self.sorted_candidates[self.elec.N_CANDIDATES - 1][1]/self.elec.N_VOTERS == 0.5 and _round == self.elec.N_CANDIDATES - self.elec.N_VACANCIES - 1):
			return 2
		elif(self.sorted_candidates[self.elec.N_CANDIDATES - 1][1]/self.elec.N_VOTERS > 0.5):
			return 1
		else:
			self.elec.excluded.add(self.sorted_candidates[_round][self.elec.CANDIDATE_INDEX])
			for voter_index in self.votes[self.sorted_candidates[_round][self.elec.CANDIDATE_INDEX]]:
				if voter_index in self.rankings_changed:
					for candidate in reversed(self.rankings_changed[voter_index]):
						if candidate[self.elec.CANDIDATE_INDEX] not in self.elec.excluded:
							self.candidates[candidate[self.elec.CANDIDATE_INDEX]] += 1
							self.votes[candidate[self.elec.CANDIDATE_INDEX]].add(voter_index)
							break
						else:
							continue
				else:
					for candidate in reversed(self.elec.sorted_voters[voter_index]):
						if candidate[self.elec.CANDIDATE_INDEX] not in self.elec.excluded:
							self.candidates[candidate[self.elec.CANDIDATE_INDEX]] += 1
							self.votes[candidate[self.elec.CANDIDATE_INDEX]].add(voter_index)
							break
						else:
							continue
					
			self.sorted_candidates = self.elec.sort_candidates(self.candidates)
			return 0

	def _apply_tactical_votes(self):
		print("::::::::APPLYING TACTICAL VOTES...")
		self.votes = copy.deepcopy(self.votes_copy)
		self.candidates = copy.deepcopy(self.elec.candidates)
		self.elec.rounds = []
		self.elec.excluded = set()
		t_votes_changed = 0
		pos = set()
		for index, perc in enumerate(self.elec.tactical_vote_percentages):
			if perc > 0:
				pos.add(index)
		# print("pos: ", pos)
		for candidate in self.elec.candidates:
			if candidate not in self.leading_candidates:
				for voter_index in self.votes_copy[candidate]:
					raised = None
					for candidate_tuple in reversed(self.elec.sorted_voters[voter_index]):
						if candidate_tuple[self.elec.CANDIDATE_INDEX] in self.leading_candidates:
							if candidate_tuple[self.elec.CANDIDATE_INDEX] in pos:
								if random.random() < self.elec.tactical_vote_percentages[candidate_tuple[self.elec.CANDIDATE_INDEX]]:
									# print(self.elec.sorted_voters[voter_index])
									ranking = [None]*self.elec.N_CANDIDATES
									ranking[-1] = (candidate_tuple[self.elec.CANDIDATE_INDEX], self.elec.voters[voter_index][candidate_tuple[self.elec.CANDIDATE_INDEX]])
									raised = candidate_tuple[self.elec.CANDIDATE_INDEX]
									self.votes[candidate].remove(voter_index)
									self.candidates[candidate] -= 1
									self.votes[candidate_tuple[self.elec.CANDIDATE_INDEX]].add(voter_index)
									self.candidates[candidate_tuple[self.elec.CANDIDATE_INDEX]] += 1
									break
								break
							break
					if raised != None:
						# print("raised: ", raised)
						for _candidate in self.leading_candidates:
							if _candidate != ranking[-1][0]:
								ranking[0] = (_candidate, self.elec.voters[voter_index][_candidate])
								buried = _candidate
								break
						i = 1
						# print("buried: ", buried)
						for candidate_tuple in self.elec.sorted_voters[voter_index]:
							# print(i)
							# print(candidate_tuple)
							if candidate_tuple[self.elec.CANDIDATE_INDEX] in [raised, buried]:
								continue
							else:
								ranking[i] = (candidate_tuple[self.elec.CANDIDATE_INDEX], self.elec.voters[voter_index][candidate_tuple[self.elec.CANDIDATE_INDEX]])
								i += 1
						self.rankings_changed[voter_index] = ranking
						# print("new: ", ranking)
			elif candidate in pos:
				for voter_index in self.votes_copy[candidate]:
					if random.random() < self.elec.tactical_vote_percentages[candidate]:
						# print(self.elec.sorted_voters[voter_index])
						for _candidate in self.leading_candidates:
							if _candidate != candidate:
								ranking = [None]*self.elec.N_CANDIDATES
								ranking[0] = (_candidate, self.elec.voters[voter_index][_candidate])
								buried = _candidate
								break
						i = 1
						# print("buried: ", buried)
						for candidate_tuple in self.elec.sorted_voters[voter_index]:
							# print(i)
							# print(candidate_tuple)
							if candidate_tuple[self.elec.CANDIDATE_INDEX] == buried:
								continue
							else:
								ranking[i] = (candidate_tuple[self.elec.CANDIDATE_INDEX], self.elec.voters[voter_index][candidate_tuple[self.elec.CANDIDATE_INDEX]])
								i += 1
						self.rankings_changed[voter_index] = ranking
						# print("new: ", ranking)

	def _set_leading_candidates(self):
		for leader in self.elec.rounds[-1]:
			self.leading_candidates.append(leader[0])
		print("leading: ", self.leading_candidates)

	def _simulate_rounds(self):
		self.sorted_candidates = self.elec.sort_candidates(self.candidates)
		# FOR SINGLE WINNER ELECTIONS
		if(self.elec.N_VACANCIES < 2):
			for _round in range(self.elec.N_CANDIDATES - self.elec.N_VACANCIES):
				result = self._count_votes(_round)
				if(result == 1):
					winners = []
					vacancies = self.elec.N_VACANCIES
					for candidate in reversed(self.sorted_candidates):
						if vacancies == 0:
							break
						winners.append(candidate[0])
						vacancies -= 1
					mean, satisfaction_rate, chose_best = self.elec.get_mean(winners = winners)
					return mean, satisfaction_rate, chose_best
				elif(result == 0):
					# print("eliminate last place")
					continue
				else:
					# print("TIE!")
					winners = []
					vacancies = self.elec.N_VACANCIES
					for candidate in reversed(self.sorted_candidates):
						if vacancies == 0:
							break
						winners.append(candidate[0])
						vacancies -= 1
					mean, satisfaction_rate, chose_best = self.elec.get_mean(winners = winners)
					return mean, satisfaction_rate, chose_best
		else: # FOR MULTIPLE WINNER ELECTIONS, TURNS INTO FPTP
			winners = []
			vacancies = self.elec.N_VACANCIES
			for candidate in reversed(self.sorted_candidates):
				if vacancies == 0:
					break
				winners.append(candidate[0])
				vacancies -= 1
			mean, satisfaction_rate, chose_best = self.elec.get_mean(winners = winners)
			# print("MEAN: ", mean)
			self.elec.rounds.append(self.sorted_candidates)
			return mean, satisfaction_rate, chose_best

	def simulate(self):
		print("INSTANT RUNOFF VOTING")
		start_time = time.time()
		mean = 0
		satisfaction_rate = 0

		mean, satisfaction_rate, chose_best = self._simulate_rounds()
		if self.elec.TACTICAL_VOTING:
			self._set_leading_candidates()
			self._apply_tactical_votes()
			mean, satisfaction_rate, chose_best = self._simulate_rounds()

		rout = []

		for r in self.elec.rounds:
			_round = [[], []]
			for i in range(len(r)):
				_round[0].append(self.elec.candidates_names[r[i][0]])
				_round[1].append(r[i][1])
			rout.append(_round)

		elected = rout[-1][0][-self.elec.N_VACANCIES:]

		now = time.time()
		print('IRV duration: ' + str(round(now - start_time, 2)) + ' seg' )
		return rout, mean, elected, satisfaction_rate, chose_best