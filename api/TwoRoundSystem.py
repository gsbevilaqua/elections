from api.Elections import Elections
#from Elections import Elections

class TwoRoundSystem:

	elec = None
	candidates = dict()
	sorted_candidates = []
	votes = []
	winner = -1 # INDEX OF WINNER CANDIDATE OF THE ELECTION
	second_place = -1 # INDEX OF SECOND PLACE CANDIDATE OF THE ELECTION

	def __init__(self, elec):
		self.elec = elec
		self.candidates = elec.candidates.copy()
		self.sorted_candidates = elec.sort_candidates(self.candidates)
		self.votes = elec.votes.copy()
		self.winner = self.sorted_candidates[-1][elec.CANDIDATE_INDEX]
		self.second_place = self.sorted_candidates[-2][elec.CANDIDATE_INDEX]

	def first_round(self):
		print("\nFIRST ROUND:")
		for candidate in self.sorted_candidates:
			percentage = str(candidate[self.elec.NUMBER_OF_VOTES]/self.elec.N_VOTERS)
			print("candidate " + str(candidate[self.elec.CANDIDATE_INDEX]) + ": " + str(candidate[self.elec.NUMBER_OF_VOTES]) + " votes - " + percentage + "%")
		mean = self.elec.calculate_mean(winner=self.sorted_candidates[-1][self.elec.CANDIDATE_INDEX])
		print("MEAN: ", mean)
		return self.sorted_candidates, mean
	
	def second_round(self):

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
		mean = self.elec.calculate_mean(winner = self.sorted_candidates[-1][self.elec.CANDIDATE_INDEX])
		print("MEAN: ", mean)
		return {self.sorted_candidates[-1][self.elec.CANDIDATE_INDEX] : self.sorted_candidates[-1][self.elec.NUMBER_OF_VOTES], self.sorted_candidates[-2][self.elec.CANDIDATE_INDEX] : self.sorted_candidates[-2][self.elec.NUMBER_OF_VOTES]}, mean

	def simulate(self):
		print("TWO-ROUND SYSTEM")

		fc, fm = self.first_round()
		fcout = [[], []]
		for element in fc:
			fcout[0].append(self.elec.candidates_names[int(element[0])])
			fcout[1].append(element[1])

		second_round = False
		sm = None
		scout = [[], []]
		elected = fcout[0][-self.elec.N_VACANCIES:]
		if(not self.elec.N_VACANCIES > 1):
			second_round = True
			sc, sm = self.second_round()
			for key, votes in sc.items():
				scout[0].append(self.elec.candidates_names[int(key)])
				scout[1].append(votes)
			scout[0] = [scout[0][1], scout[0][0]]
			scout[1] = [scout[1][1], scout[1][0]]
			elected = [scout[0][-1]]

		print(scout)
		print(elected)

		return fcout, fm, scout, sm, second_round, elected