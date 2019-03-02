import time
from api.Elections import Elections

class InstantRunoffVoting(Elections):

	excluded = set()
	rounds = []

	def count_votes(self, _round):
		self.rounds.append(self.sorted_candidates[_round:])
		if(self.sorted_candidates[self.N_CANDIDATES - 1][1]/self.N_VOTERS == 0.5):
			return 2
		elif(self.sorted_candidates[self.N_CANDIDATES - 1][1]/self.N_VOTERS > 0.5):
			return 1
		else:
			self.excluded.add(self.sorted_candidates[_round][self.CANDIDATE_INDEX])
			for voter_index in self.votes[self.sorted_candidates[_round][self.CANDIDATE_INDEX]]:
				available = []
				for candidate in reversed(self.sorted_voters[voter_index]):
					if candidate[self.CANDIDATE_INDEX] not in self.excluded:
						self.candidates[candidate[self.CANDIDATE_INDEX]] += 1
						self.votes[candidate[self.CANDIDATE_INDEX]].append(voter_index)
						break
					else:
						continue
					
			self.sort_candidates()
			return 0

	def calculate_mean(self, winner):
		s = 0
		for voter_index in self.votes[winner]:
			s += self.voters[voter_index][winner]
		return s/self.N_VOTERS

	def simulate(self):
		print("INSTANT RUNOFF VOTING")

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

		self.sort_candidates()
		for _round in range(self.N_CANDIDATES - 1):
			result = self.count_votes(_round)
			if(result == 1):
				print("first_place wins")
				mean = self.calculate_mean(winner = self.sorted_candidates[self.N_CANDIDATES - 1][self.CANDIDATE_INDEX])
				print("MEAN: ", mean)
				break
			elif(result == 0):
				print("eliminate last_place")
			else:
				print("TIE!")
				break

		return self.rounds, mean