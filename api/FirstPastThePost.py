import random, copy, math
from api.Elections import Elections
#from Elections import Elections

class FirstPastThePost:

	elec = None
	candidates = dict()
	sorted_candidates = []
	sorted_voters = []
	votes = dict()
	votes_copy = dict()
	leading_candidates = []

	def __init__(self, elec):
		self.elec = elec
		self.candidates = elec.candidates.copy()
		self.sorted_voters = copy.deepcopy(elec.sorted_voters)
		self.votes = copy.deepcopy(elec.votes)
		self.votes_copy = copy.deepcopy(elec.votes)
		self.sorted_candidates = elec.sort_candidates(self.candidates)

		self.leading_candidates = elec.leading_candidates

	def _set_leading_candidates(self):
		if self.elec.N_VACANCIES == 1 or self.elec.N_VACANCIES == 2:
			self.leading_candidates.append(self.sorted_candidates[-1][self.elec.CANDIDATE_INDEX])
			self.leading_candidates.append(self.sorted_candidates[-2][self.elec.CANDIDATE_INDEX])
			self.leading_candidates.append(self.sorted_candidates[-3][self.elec.CANDIDATE_INDEX])
		elif self.elec.N_VACANCIES > 2:
			for i in range(1, self.elec.N_VACANCIES + 2):
				self.leading_candidates.append(self.sorted_candidates[-i][self.elec.CANDIDATE_INDEX])
		
		print("leading: ", self.leading_candidates)

	def _count_tactical_votes(self):
		print("::::::::COUNTING TACTICAL VOTES...")
		t_votes_changed = 0
		for candidate in self.votes_copy:
			if candidate not in self.leading_candidates:
				for voter_index in self.votes_copy[candidate]:
					for index, _candidate in enumerate(reversed(self.elec.sorted_voters[voter_index])):
						if _candidate[self.elec.CANDIDATE_INDEX] in self.leading_candidates:
							if _candidate[self.elec.CANDIDATE_RANK] >= 0:
								if random.random() < self.elec.tactical_vote_percentages[_candidate[self.elec.CANDIDATE_INDEX]]:
									t_votes_changed += 1
									self.sorted_voters[voter_index][index], self.sorted_voters[voter_index][-1] = self.sorted_voters[voter_index][-1], self.sorted_voters[voter_index][index]
									self.candidates[candidate] -= 1
									self.candidates[_candidate[self.elec.CANDIDATE_INDEX]] += 1
									self.votes[candidate].remove(voter_index)
									self.votes[_candidate[self.elec.CANDIDATE_INDEX]].add(voter_index)
									break
		
		print(":::::T votes changed: ", t_votes_changed)
							
	def _count_minority_votes(self):
		print("::::::::COUNTING MINORITY VOTES...")
		m_votes_changed = 0
		half_vacancies = math.floor(self.elec.N_VACANCIES/2)

		for candidate in self.leading_candidates:
			if self.leading_candidates.index(candidate) >= half_vacancies:
				break
			for voter_index in self.votes_copy[candidate]:
				for index, _candidate in enumerate(self.sorted_voters[voter_index]):
					if _candidate[self.elec.CANDIDATE_INDEX] in self.leading_candidates:
						if self.leading_candidates.index(_candidate[self.elec.CANDIDATE_INDEX]) >= half_vacancies:
							if _candidate[self.elec.CANDIDATE_RANK] >= 0:
								if random.random() < self.elec.minority_vote_percentages[_candidate[self.elec.CANDIDATE_INDEX]]:
									m_votes_changed += 1
									self.candidates[candidate] -= 1
									self.candidates[_candidate[self.elec.CANDIDATE_INDEX]] += 1
									self.votes[candidate].remove(voter_index)
									self.votes[_candidate[self.elec.CANDIDATE_INDEX]].add(voter_index)
									self.sorted_voters.append(self.sorted_voters[voter_index].pop(index))
									break
							else:
								break
					else:
						if _candidate[self.elec.CANDIDATE_RANK] >= 0:
							if random.random() < self.elec.minority_vote_percentages[_candidate[self.elec.CANDIDATE_INDEX]]:
								m_votes_changed += 1
								self.candidates[candidate] -= 1
								self.candidates[_candidate[self.elec.CANDIDATE_INDEX]] += 1
								self.votes[candidate].remove(voter_index)
								self.votes[_candidate[self.elec.CANDIDATE_INDEX]].add(voter_index)
								self.sorted_voters.append(self.sorted_voters[voter_index].pop(index))
								break
			
		print(":::::M votes changed: ", m_votes_changed)

	def simulate(self):
		print("FIRST PAST THE POST")

		print(self.elec.candidates_names)

		self._set_leading_candidates()
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
		mean, satisfaction_rate = self.elec.calculate_mean(winners = winners)

		elected = out[0][-self.elec.N_VACANCIES:]

		return out, mean, elected, satisfaction_rate