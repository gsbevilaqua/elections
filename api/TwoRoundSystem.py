import random, copy, math
from api.Elections import Elections
#from Elections import Elections

class TwoRoundSystem:

	elec = None
	candidates = dict()
	sorted_candidates = []
	sorted_voters = []
	votes = dict()
	votes_copy = dict()
	winner = -1 # INDEX OF WINNER CANDIDATE OF THE ELECTION
	second_place = -1 # INDEX OF SECOND PLACE CANDIDATE OF THE ELECTION
	leading_candidates = []

	def __init__(self, elec):
		self.elec = elec
		self.candidates = elec.candidates.copy()
		self.sorted_voters = copy.deepcopy(elec.sorted_voters)
		self.votes = copy.deepcopy(elec.votes)
		self.votes_copy = copy.deepcopy(elec.votes)
		self.sorted_candidates = elec.sort_candidates(self.candidates)
		self.winner = self.sorted_candidates[-1][elec.CANDIDATE_INDEX]
		self.second_place = self.sorted_candidates[-2][elec.CANDIDATE_INDEX]
		self.leading_candidates = elec.leading_candidates

	def _first_round(self):
		print("\nFIRST ROUND:")
		self._set_leading_candidates()
		if self.elec.N_CANDIDATES > 3 and self.elec.TACTICAL_VOTING:
			self._count_tactical_votes()
		if self.elec.N_VACANCIES > 1 and self.elec.MINORITY_VOTING:
			self._count_minority_votes()
		self.sorted_candidates = self.elec.sort_candidates(self.candidates)
		self.winner = self.sorted_candidates[-1][self.elec.CANDIDATE_INDEX]
		self.second_place = self.sorted_candidates[-2][self.elec.CANDIDATE_INDEX]
		print(self.sorted_candidates)
		winners = []
		vacancies = self.elec.N_VACANCIES
		for candidate in reversed(self.sorted_candidates):
			percentage = str(candidate[self.elec.NUMBER_OF_VOTES]/self.elec.N_VOTERS)
			print("candidate " + str(candidate[self.elec.CANDIDATE_INDEX]) + ": " + str(candidate[self.elec.NUMBER_OF_VOTES]) + " votes - " + percentage + "%")
			if vacancies > 0:
				winners.append(candidate[0])
		mean, satisfaction_rate = self.elec.calculate_mean(winners = winners)
		print("MEAN: ", mean)
		return self.sorted_candidates, mean, satisfaction_rate
	
	def _second_round(self):
		for candidate in self.votes:
			if candidate != self.winner and candidate != self.second_place:
				for voter_index in self.votes[candidate]:
					for index2, candidate in enumerate(reversed(self.elec.sorted_voters[voter_index])):
						if candidate[self.elec.CANDIDATE_INDEX] == self.winner:
							self.candidates[self.winner] += 1
							self.votes[self.winner].add(voter_index)
							break
						elif candidate[self.elec.CANDIDATE_INDEX] == self.second_place:
							self.candidates[self.second_place] += 1
							self.votes[self.second_place].add(voter_index)
							break

		print("\nSECOND ROUND:")

		self.sorted_candidates = self.elec.sort_candidates(self.candidates)
		print(self.sorted_candidates)
		winners = []
		vacancies = self.elec.N_VACANCIES
		for candidate in reversed(self.sorted_candidates):
			if vacancies == 0:
				break
			winners.append(candidate[0])
		mean, satisfaction_rate = self.elec.calculate_mean(winners = winners)
		print("MEAN: ", mean)
		return {self.sorted_candidates[-1][self.elec.CANDIDATE_INDEX] : self.sorted_candidates[-1][self.elec.NUMBER_OF_VOTES], self.sorted_candidates[-2][self.elec.CANDIDATE_INDEX] : self.sorted_candidates[-2][self.elec.NUMBER_OF_VOTES]}, mean, satisfaction_rate

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

		for candidate in self.leading_candidates:
			if self.leading_candidates.index(candidate) >= math.floor(self.elec.N_VACANCIES/2):
				break
			for voter_index in self.votes_copy[candidate]:
				for index, _candidate in enumerate(self.sorted_voters[voter_index]):
					if _candidate[self.elec.CANDIDATE_INDEX] in self.leading_candidates:
						if self.leading_candidates.index(_candidate[self.elec.CANDIDATE_INDEX]) >= math.floor(self.elec.N_VACANCIES/2):
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
		print("TWO-ROUND SYSTEM")

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
		if(not self.elec.N_VACANCIES > 1):
			second_round = True
			sc, sm, ssr = self._second_round()
			for key, votes in sc.items():
				scout[0].append(self.elec.candidates_names[int(key)])
				scout[1].append(votes)
			scout[0] = [scout[0][1], scout[0][0]]
			scout[1] = [scout[1][1], scout[1][0]]
			elected = [scout[0][-1]]

		print("second round: ", scout)
		print("elected:", elected)
		print("og candidates: ", self.elec.candidates)
		print("my candidates: ", self.candidates)

		return fcout, fm, scout, sm, second_round, elected, fsr, ssr