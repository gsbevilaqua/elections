import random, copy
from api.Elections import Elections
#from Elections import Elections

class ScoreVoting:

    elec = None
    candidates = dict()
    sorted_candidates = []
    sorted_voters = []

    def __init__(self, elec):
        self.elec = elec
        self.sorted_voters = copy.deepcopy(elec.sorted_voters)

    def _apply_tactical_votes(self):
        print("::::::::APPLYING TACTICAL VOTES...")
        t_votes_changed = 0
        for voter_index, voter in enumerate(self.elec.sorted_voters):
            if random.random() < self.elec.tactical_vote_percentages[voter[-1][self.elec.CANDIDATE_INDEX]]:
                t_votes_changed += 1
                for candidate_index, candidate in enumerate(reversed(voter)):
                    if candidate_index == 0:
                        continue
                    else:
                        self.sorted_voters[voter_index][-(candidate_index + 1)] = (voter[-(candidate_index + 1)][self.elec.CANDIDATE_INDEX], -10)

		
        print(":::::ScoreBased T votes changed: ", t_votes_changed)

    def _sum_candidates_scores(self):
        for index in range(self.elec.N_CANDIDATES):
            self.candidates[index] = 0

        for voter in self.sorted_voters:
            for candidate in voter:
                self.candidates[candidate[self.elec.CANDIDATE_INDEX]] += candidate[self.elec.CANDIDATE_RANK]

    def simulate(self):
        print("SCORE VOTING SYSTEM")

        if self.elec.TACTICAL_VOTING:
            self._apply_tactical_votes()
        self._sum_candidates_scores()
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