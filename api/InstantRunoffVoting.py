from api.Elections import Elections
#from Elections import Elections

class InstantRunoffVoting(Elections):	

	elec = None
	candidates = dict()
	sorted_candidates = []
	votes = []

	def __init__(self, elec):
		self.elec = elec
		self.candidates = elec.candidates.copy()
		self.votes = elec.votes.copy()

	def _count_votes(self, _round):
		self.elec.rounds.append(self.sorted_candidates[_round:])
		if(self.sorted_candidates[self.elec.N_CANDIDATES - 1][1]/self.elec.N_VOTERS == 0.5):
			return 2
		elif(self.sorted_candidates[self.elec.N_CANDIDATES - 1][1]/self.elec.N_VOTERS > 0.5):
			return 1
		else:
			self.elec.excluded.add(self.sorted_candidates[_round][self.elec.CANDIDATE_INDEX])
			for voter_index in self.votes[self.sorted_candidates[_round][self.elec.CANDIDATE_INDEX]]:
				for candidate in reversed(self.elec.sorted_voters[voter_index]):
					if candidate[self.elec.CANDIDATE_INDEX] not in self.elec.excluded:
						self.candidates[candidate[self.elec.CANDIDATE_INDEX]] += 1
						self.votes[candidate[self.elec.CANDIDATE_INDEX]].add(voter_index)
						break
					else:
						continue
					
			self.sorted_candidates = self.elec.sort_candidates(self.candidates)
			print(self.sorted_candidates)
			return 0

	def simulate(self):
		print("INSTANT RUNOFF VOTING")

		mean = 0

		self.sorted_candidates = self.elec.sort_candidates(self.candidates)
		print(self.sorted_candidates)
		for _round in range(self.elec.N_CANDIDATES - self.elec.N_VACANCIES):
			result = self._count_votes(_round)
			if(result == 1):
				print("first_place wins")
				#e = [lambda x: len(x) for x in self.votes]
				#print(":::e: ", e)
				for e in self.votes:
					print(len(self.votes[e]))
				mean = self.elec.calculate_mean(winner = self.sorted_candidates[-1][self.elec.CANDIDATE_INDEX])
				print("MEAN: ", mean)
				break
			elif(result == 0):
				print("eliminate last_place")
			else:
				print("TIE!")
				mean = self.elec.calculate_mean(winner = self.sorted_candidates[-1][self.elec.CANDIDATE_INDEX])
				print("MEAN: ", mean)
				break

		rout = []

		for r in self.elec.rounds:
			_round = [[], []]
			for i in range(len(r)):
				_round[0].append(self.elec.candidates_names[r[i][0]])
				_round[1].append(r[i][1])
			rout.append(_round)

		elected = rout[-1][0][-self.elec.N_VACANCIES:]

		return rout, mean, elected