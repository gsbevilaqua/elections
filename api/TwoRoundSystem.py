import random, copy, math, time
from api.Elections import Elections
#from Elections import Elections # used for testing

class TwoRoundSystem:

	elec = None # ELECTIONS OBJECT
	candidates = dict() # DICTIONARY OF KEY -> INDEX OF CANDIDATE, VALUE -> NUMBER OF VOTES
	sorted_candidates = [] # LIST OF CANDIDATES IN ORDER FROM LEAST VOTED TO MOST VOTED
	votes = dict() # DICTIONARY OF KEY -> INDEX OF CANDIDATE, VALUE -> SET WITH THE INDICES OF THE VOTERS THAT VOTED FOR THIS CANDIDATE
	votes_copy = dict() # COPY OF VOTES DICT
	t_votes_changed = 0 # NUMBER OF VOTES CHANGED BEACAUSE OF TACTICAL VOTING
	m_votes_changed = 0 # NUMBER OF VOTES CHANGED BEACAUSE OF MINORITY VOTING
	rankings_changed = dict()

	winner = -1 # INDEX OF WINNER CANDIDATE OF THE ELECTION
	second_place = -1 # INDEX OF SECOND PLACE CANDIDATE OF THE ELECTION

	def __init__(self, elec):
		start_time = time.time()
		self.elec = elec
		self.candidates = elec.candidates.copy()
		self.votes = copy.deepcopy(elec.votes)
		self.votes_copy = copy.deepcopy(elec.votes)
		self.sorted_candidates = elec.sorted_candidates
		self.winner = self.sorted_candidates[-1][elec.CANDIDATE_INDEX]
		self.second_place = self.sorted_candidates[-2][elec.CANDIDATE_INDEX]
		print('TRS init: ' + str(round(time.time() - start_time, 2)) + ' seg' )

	def _first_round(self):
		# print("\nFIRST ROUND:")
		if self.elec.N_CANDIDATES > 3 and self.elec.TACTICAL_VOTING:
			self._count_tactical_votes()
		if self.elec.N_VACANCIES > 1 and self.elec.MINORITY_VOTING:
			self._count_minority_votes()
		self.sorted_candidates = self.elec.sort_candidates(self.candidates)
		self.winner = self.sorted_candidates[-1][self.elec.CANDIDATE_INDEX]
		self.second_place = self.sorted_candidates[-2][self.elec.CANDIDATE_INDEX]
		# print(self.sorted_candidates)
		winners = []
		vacancies = self.elec.N_VACANCIES
		for candidate in reversed(self.sorted_candidates):
			percentage = str(candidate[self.elec.NUMBER_OF_VOTES]/self.elec.N_VOTERS)
			# print("candidate " + str(candidate[self.elec.CANDIDATE_INDEX]) + ": " + str(candidate[self.elec.NUMBER_OF_VOTES]) + " votes - " + percentage + "%")
			if vacancies > 0:
				winners.append(candidate[0])
			vacancies -= 1
		mean, satisfaction_rate = self.elec.calculate_mean(winners = winners)
		# print("MEAN: ", mean)
		return self.sorted_candidates, mean, satisfaction_rate
	
	def _second_round(self):
		for candidate in self.votes:
			if candidate != self.winner and candidate != self.second_place:
				for voter_index in self.votes[candidate]:
					if voter_index in self.rankings_changed:
						ranking = self.rankings_changed[voter_index]
					else:
						ranking = self.elec.sorted_voters[voter_index]
					for index2, candidate in enumerate(reversed(ranking)):
						if candidate[self.elec.CANDIDATE_INDEX] == self.winner:
							self.candidates[self.winner] += 1
							self.votes[self.winner].add(voter_index)
							break
						elif candidate[self.elec.CANDIDATE_INDEX] == self.second_place:
							self.candidates[self.second_place] += 1
							self.votes[self.second_place].add(voter_index)
							break

		# print("\nSECOND ROUND:")

		self.sorted_candidates = self.elec.sort_candidates(self.candidates)
		# print(self.sorted_candidates)
		winners = []
		vacancies = self.elec.N_VACANCIES
		for candidate in reversed(self.sorted_candidates):
			if vacancies == 0:
				break
			winners.append(candidate[0])
			vacancies -= 1
		mean, satisfaction_rate = self.elec.calculate_mean(winners = winners)
		# print("MEAN: ", mean)
		return {self.sorted_candidates[-1][self.elec.CANDIDATE_INDEX] : self.sorted_candidates[-1][self.elec.NUMBER_OF_VOTES], self.sorted_candidates[-2][self.elec.CANDIDATE_INDEX] : self.sorted_candidates[-2][self.elec.NUMBER_OF_VOTES]}, mean, satisfaction_rate

	# CANDIDATES THAT ARE NOT IN 'leading_candidates' LIST LOSE VOTES TO LEADING CANDIDATES BASED ON LEADING CANDIDATES TACTICAL VOTING PERCENTAGE PARAMETER
	def _count_tactical_votes(self):
		print("::::::::COUNTING TACTICAL VOTES...")
		self.t_votes_changed = 0
		for candidate in self.votes_copy:
			if candidate not in self.elec.leading_candidates:
				for voter_index in self.votes_copy[candidate]:
					for index, _candidate in enumerate(reversed(self.elec.sorted_voters[voter_index])):
						if _candidate[self.elec.CANDIDATE_INDEX] in self.elec.leading_candidates and _candidate[self.elec.CANDIDATE_RANK] >= 0 and random.random() < self.elec.tactical_vote_percentages[_candidate[self.elec.CANDIDATE_INDEX]]:
							self.t_votes_changed += 1
							self.rankings_changed[voter_index] = self.elec.sorted_voters[voter_index]
							self.rankings_changed[voter_index][index], self.rankings_changed[voter_index][-1] = self.rankings_changed[voter_index][-1], self.rankings_changed[voter_index][index]
							self.candidates[candidate] -= 1
							self.candidates[_candidate[self.elec.CANDIDATE_INDEX]] += 1
							self.votes[candidate].remove(voter_index)
							self.votes[_candidate[self.elec.CANDIDATE_INDEX]].add(voter_index)
							break
		
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
					ranking = self.elec.sorted_voters[voter_index]
				for index, _candidate in enumerate(reversed(ranking)):
					if _candidate[self.elec.CANDIDATE_INDEX] not in self.elec.leading_candidates or (_candidate[self.elec.CANDIDATE_INDEX] in self.elec.leading_candidates and self.elec.leading_candidates.index(_candidate[self.elec.CANDIDATE_INDEX]) >= half_vacancies):
						if _candidate[self.elec.CANDIDATE_RANK] >= 0:
							if random.random() < self.elec.minority_vote_percentages[_candidate[self.elec.CANDIDATE_INDEX]]:
								self.m_votes_changed += 1
								self.candidates[candidate] -= 1
								self.candidates[_candidate[self.elec.CANDIDATE_INDEX]] += 1
								self.votes[candidate].remove(voter_index)
								self.votes[_candidate[self.elec.CANDIDATE_INDEX]].add(voter_index)
								if voter_index in self.rankings_changed:
									self.rankings_changed[voter_index].append(self.rankings_changed[voter_index].pop(index))
								else:
									self.rankings_changed[voter_index] = self.elec.sorted_voters[voter_index]
									self.rankings_changed[voter_index].append(self.rankings_changed[voter_index].pop(index))
								break
							else:
								break
						else:
							break

		print(":::::M votes changed: ", self.m_votes_changed)

	def simulate(self):
		print("TWO-ROUND SYSTEM")
		start_time = time.time()
		fc, fm, fsr = self._first_round()
		fcout = [[], []]
		for element in fc:
			fcout[0].append(self.elec.candidates_names[int(element[self.elec.CANDIDATE_INDEX])])
			fcout[1].append(element[self.elec.NUMBER_OF_VOTES])

		second_round = False
		sm = None
		scout = [[], []]
		ssr = None
		elected = fcout[0][-self.elec.N_VACANCIES:]
		if(not self.elec.N_VACANCIES > 1 and self.sorted_candidates[-1][self.elec.NUMBER_OF_VOTES]/self.elec.N_VOTERS <= 0.5):
			second_round = True
			sc, sm, ssr = self._second_round()
			for key, votes in sc.items():
				scout[0].append(self.elec.candidates_names[int(key)])
				scout[1].append(votes)
			scout[0] = [scout[0][1], scout[0][0]]
			scout[1] = [scout[1][1], scout[1][0]]
			elected = [scout[0][-1]]

		# print("second round: ", scout)
		# print("elected:", elected)
		# print("og candidates: ", self.elec.candidates)
		# print("my candidates: ", self.candidates)
		now = time.time()
		print('TRS duration: ' + str(round(now - start_time, 2)) + ' seg' )
		return fcout, fm, scout, sm, second_round, elected, fsr, ssr