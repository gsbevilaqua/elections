import copy, time
from api.Elections import Elections
#from Elections import Elections # used for testing

class InstantRunoffVoting(Elections):	

	elec = None
	candidates = dict()
	sorted_candidates = []
	votes = dict()

	def __init__(self, elec):
		start_time = time.time()
		self.elec = elec
		self.candidates = elec.candidates.copy()
		self.votes = copy.deepcopy(elec.votes)
		print('IRV init: ' + str(round(time.time() - start_time, 2)) + ' seg' )

	def _count_votes(self, _round):
		self.elec.rounds.append(self.sorted_candidates[_round:])
		# print(self.sorted_candidates[self.elec.N_CANDIDATES - 1][1]/self.elec.N_VOTERS)
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
			# print(self.sorted_candidates)
			return 0

	def simulate(self):
		print("INSTANT RUNOFF VOTING")
		start_time = time.time()
		mean = 0
		satisfaction_rate = 0

		self.sorted_candidates = self.elec.sort_candidates(self.candidates)
		# print(self.sorted_candidates)
		if(self.elec.N_VACANCIES < 2):
			for _round in range(self.elec.N_CANDIDATES - self.elec.N_VACANCIES):
				result = self._count_votes(_round)
				if(result == 1):
					# print("first_place wins")
					#e = [lambda x: len(x) for x in self.votes]
					#print(":::e: ", e)
					# for e in self.votes:
					# 	print(len(self.votes[e]))
					winners = []
					vacancies = self.elec.N_VACANCIES
					for candidate in reversed(self.sorted_candidates):
						if vacancies == 0:
							break
						winners.append(candidate[0])
						vacancies -= 1
					mean, satisfaction_rate = self.elec.calculate_mean(winners = winners)
					# print("MEAN: ", mean)
					break
				elif(result == 0):
				# 	# print("eliminate last_place")
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
					mean, satisfaction_rate = self.elec.calculate_mean(winners = winners)
					# print("MEAN: ", mean)
					break
		else:
			winners = []
			vacancies = self.elec.N_VACANCIES
			for candidate in reversed(self.sorted_candidates):
				if vacancies == 0:
					break
				winners.append(candidate[0])
				vacancies -= 1
			mean, satisfaction_rate = self.elec.calculate_mean(winners = winners)
			# print("MEAN: ", mean)
			self.elec.rounds.append(self.sorted_candidates)

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
		return rout, mean, elected, satisfaction_rate