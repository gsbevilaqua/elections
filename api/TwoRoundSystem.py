import time
from api.Elections import Elections

class TwoRoundSystem(Elections):

	def first_round(self):
		self.sort_candidates()
		print("\nFIRST ROUND:")
		for candidate in self.sorted_candidates:
			percentage = str(candidate[self.NUMBER_OF_VOTES]/self.N_VOTERS)
			print("candidate " + str(candidate[self.CANDIDATE_INDEX]) + ": " + str(candidate[self.NUMBER_OF_VOTES]) + " votes - " + percentage + "%")
		mean = self.calculate_mean()
		print("MEAN: ", mean)
		return self.sorted_candidates, mean
	
	def second_round(self):
		n_votes_candidate1 = 0
		n_votes_candidate2 = 0
		first_voters = []
		second_voters = []

		for candidate in self.votes:
			if candidate != self.winner and candidate != self.second_place:
				for voter_index in self.votes[candidate]:
					for index2, candidate in enumerate(reversed(self.sorted_voters[voter_index])):
						if candidate[self.CANDIDATE_INDEX] == self.winner:
							n_votes_candidate1 += 1
							first_voters.append(voter_index)
							break
						elif candidate[self.CANDIDATE_INDEX] == self.second_place:
							n_votes_candidate2 += 1
							second_voters.append(voter_index)
							break

		print("\nSECOND ROUND:")
		second_round_winner, winner_votes, second_votes = self.count_votes_second_round(n_votes_candidate1, n_votes_candidate2)

		if(second_round_winner == 1):
			first_round_voters = self.calculate_mean(second_round_share = True)
			mean = self.calculate_second_mean(first_voters, first_round_voters, self.winner)
			print("MEAN: ", mean)
		else:
			first_round_voters = self.calculate_mean(second_round_share = True, second_place_is_the_winner_actually = True)
			mean = self.calculate_second_mean(second_voters, first_round_voters, self.second_place)
			print("MEAN: ", mean)

		return {self.winner : winner_votes, self.second_place : second_votes}, mean


	def count_votes_second_round(self, cand1, cand2):
		cand1_votes = self.sorted_candidates[-1][self.CANDIDATE_RANK] + cand1
		cand2_votes = self.sorted_candidates[-2][self.CANDIDATE_RANK] + cand2
		self.winner = (self.sorted_candidates[-1][self.CANDIDATE_INDEX], cand1_votes) if (cand1_votes > cand2_votes) else (self.sorted_candidates[-2][self.CANDIDATE_INDEX], cand2_votes)
		self.second_place = (self.sorted_candidates[-2][self.CANDIDATE_INDEX], cand2_votes) if (cand1_votes > cand2_votes) else (self.sorted_candidates[-1][self.CANDIDATE_INDEX], cand1_votes)
		print("Winner: " + str(self.winner[0]) + " with " + str(self.winner[1]) + " votes")
		print("Second place: " + str(self.second_place[self.CANDIDATE_INDEX]) + " with " + str(self.second_place[self.CANDIDATE_RANK]) + " votes")

		if(cand1_votes >= cand2_votes):
			return 1, cand1_votes, cand2_votes
		else:
			return 2, cand2_votes, cand1_votes

	# CALCULATES MEAN AND MEAN2 FOR FIRST ROUND - MEAN IS (SUM OF WINNER RATINGS FROM VOTERS WHO VOTED FOR THE WINNER)/NUMBER OF VOTERS / MEAN2 IS (SUM OF WINNER RATINGS)/NUMBER OF VOTERS
	def calculate_mean(self, second_round_share = False, second_place_is_the_winner_actually = False):
		self.winner = self.sorted_candidates[self.N_CANDIDATES - 1][self.CANDIDATE_INDEX]
		self.second_place = self.sorted_candidates[self.N_CANDIDATES - 2][self.CANDIDATE_INDEX]
		s = 0

		if(second_place_is_the_winner_actually == False):
			for voter in self.sorted_voters:
				if(voter[self.N_CANDIDATES - 1][self.CANDIDATE_INDEX] == self.winner):
					s += voter[self.N_CANDIDATES - 1][self.CANDIDATE_RANK]
			mean = s/self.N_VOTERS
		else:
			for voter in self.sorted_voters:
				if(voter[self.N_CANDIDATES - 1][self.CANDIDATE_INDEX] == self.second_place):
					s += voter[self.N_CANDIDATES - 1][self.CANDIDATE_RANK]

		if(second_round_share):
			return s

		return mean

	# CALCULATES MEAN FOR SECOND ROUND
	def calculate_second_mean(self, second_round_winner_voters, first_round_voters, winner):
		s = first_round_voters
		for voter in second_round_winner_voters:
			s += self.voters[voter][winner]
		return s/self.N_VOTERS

	def simulate(self):
		print("TWO-ROUND SYSTEM")

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

		fc, fm = self.first_round()
		sc, sm = self.second_round()

		fcout = []
		scout = []

		for element in fc:
			fcout.append(["Candidate " + str(element[0]), element[1]])
		for key, votes in sc.items():
			scout.append(["Candidate " + str(key), votes])

		return fcout, fm, scout, sm