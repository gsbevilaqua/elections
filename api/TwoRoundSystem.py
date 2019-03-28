from api.Elections import Elections
#from Elections import Elections

class TwoRoundSystem:

	elec = None
	sorted_candidates = []
	winner = -1 # INDEX OF WINNER CANDIDATE OF THE ELECTION
	second_place = -1 # INDEX OF SECOND PLACE CANDIDATE OF THE ELECTION

	def __init__(self, elec):
		self.elec = elec
		self.sorted_candidates = elec.sort_candidates(self.elec.candidates)

	def first_round(self):
		print("\nFIRST ROUND:")
		for candidate in self.sorted_candidates:
			percentage = str(candidate[self.elec.NUMBER_OF_VOTES]/self.elec.N_VOTERS)
			print("candidate " + str(candidate[self.elec.CANDIDATE_INDEX]) + ": " + str(candidate[self.elec.NUMBER_OF_VOTES]) + " votes - " + percentage + "%")
		mean = self.calculate_mean()
		print("MEAN: ", mean)
		return self.sorted_candidates, mean
	
	def second_round(self):
		n_votes_candidate1 = 0
		n_votes_candidate2 = 0
		first_voters = []
		second_voters = []

		for candidate in self.elec.votes:
			if candidate != self.winner and candidate != self.second_place:
				for voter_index in self.elec.votes[candidate]:
					for index2, candidate in enumerate(reversed(self.elec.sorted_voters[voter_index])):
						if candidate[self.elec.CANDIDATE_INDEX] == self.winner:
							n_votes_candidate1 += 1
							first_voters.append(voter_index)
							break
						elif candidate[self.elec.CANDIDATE_INDEX] == self.second_place:
							n_votes_candidate2 += 1
							second_voters.append(voter_index)
							break

		print("\nSECOND ROUND:")
		second_round_winner, winner_votes, second_votes = self.count_votes_second_round(n_votes_candidate1, n_votes_candidate2)

		if(second_round_winner == 1):
			first_round_voters = self.calculate_mean(second_round_share = True)
			mean = self.calculate_second_mean(first_voters, first_round_voters, self.winner)
			print("MEAN: ", mean)
			return {self.winner : winner_votes, self.second_place : second_votes}, mean
		else:
			first_round_voters = self.calculate_mean(second_round_share = True, second_place_is_the_winner_actually = True)
			mean = self.calculate_second_mean(second_voters, first_round_voters, self.second_place)
			print("MEAN: ", mean)
			return {self.second_place : winner_votes, self.winner : second_votes}, mean


	def count_votes_second_round(self, cand1, cand2):
		cand1_votes = self.sorted_candidates[-1][self.elec.NUMBER_OF_VOTES] + cand1
		cand2_votes = self.sorted_candidates[-2][self.elec.NUMBER_OF_VOTES] + cand2
		self.winner = (self.sorted_candidates[-1][self.elec.CANDIDATE_INDEX], cand1_votes) if (cand1_votes >= cand2_votes) else (self.sorted_candidates[-2][self.elec.CANDIDATE_INDEX], cand2_votes)
		self.second_place = (self.sorted_candidates[-2][self.elec.CANDIDATE_INDEX], cand2_votes) if (cand1_votes > cand2_votes) else (self.sorted_candidates[-1][self.elec.CANDIDATE_INDEX], cand1_votes)
		print("Winner: " + str(self.winner[self.elec.CANDIDATE_INDEX]) + " with " + str(self.winner[self.elec.NUMBER_OF_VOTES]) + " votes")
		print("Second place: " + str(self.second_place[self.elec.CANDIDATE_INDEX]) + " with " + str(self.second_place[self.elec.NUMBER_OF_VOTES]) + " votes")

		if(cand1_votes >= cand2_votes):
			return 1, cand1_votes, cand2_votes
		else:
			return 2, cand2_votes, cand1_votes

	# CALCULATES MEAN AND MEAN2 FOR FIRST ROUND - MEAN IS (SUM OF WINNER RATINGS FROM VOTERS WHO VOTED FOR THE WINNER)/NUMBER OF VOTERS / MEAN2 IS (SUM OF WINNER RATINGS)/NUMBER OF VOTERS
	def calculate_mean(self, second_round_share = False, second_place_is_the_winner_actually = False):
		self.winner = self.sorted_candidates[self.elec.N_CANDIDATES - 1][self.elec.CANDIDATE_INDEX]
		self.second_place = self.sorted_candidates[self.elec.N_CANDIDATES - 2][self.elec.CANDIDATE_INDEX]
		s = 0

		if(second_place_is_the_winner_actually == False):
			for voter in self.elec.sorted_voters:
				if(voter[self.elec.N_CANDIDATES - 1][self.elec.CANDIDATE_INDEX] == self.winner):
					s += voter[self.elec.N_CANDIDATES - 1][self.elec.CANDIDATE_RANK]
			mean = s/self.elec.N_VOTERS
		else:
			for voter in self.elec.sorted_voters:
				if(voter[self.elec.N_CANDIDATES - 1][self.elec.CANDIDATE_INDEX] == self.second_place):
					s += voter[self.elec.N_CANDIDATES - 1][self.elec.CANDIDATE_RANK]

		if(second_round_share):
			return s

		return mean

	# CALCULATES MEAN FOR SECOND ROUND
	def calculate_second_mean(self, second_round_winner_voters, first_round_voters, winner):
		s = first_round_voters
		for voter in second_round_winner_voters:
			s += self.elec.voters[voter][winner]
		return s/self.elec.N_VOTERS

	def simulate(self):
		print("TWO-ROUND SYSTEM")

		fc, fm = self.first_round()
		fcout = [[], []]
		for element in fc:
			fcout[0].append("Candidate " + str(element[0]))
			fcout[1].append(element[1])

		second_round = False
		sm = None
		scout = [[], []]
		if(not self.elec.N_VACANCIES > 1):
			second_round = True
			sc, sm = self.second_round()
			for key, votes in sc.items():
				scout[0].append("Candidate " + str(key))
				scout[1].append(votes)

		return fcout, fm, scout, sm, second_round