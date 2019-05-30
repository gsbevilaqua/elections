import random, copy
from api.Elections import Elections
#from Elections import Elections

class ApprovalVoting:

    elec = None
    candidates = dict()
    sorted_candidates = []
    sorted_voters = []

    def __init__(self, elec):
        self.elec = elec
        self.sorted_voters = copy.deepcopy(elec.sorted_voters)

    def _count_votes(self):
        for index in range(self.elec.N_CANDIDATES):
            self.candidates[index] = 0

        t_votes_changed = 0
        for voter in self.sorted_voters:
            if random.random() < self.elec.tactical_vote_percentages[voter[-1][self.elec.CANDIDATE_INDEX]]:
                t_votes_changed += 1
                self.candidates[voter[-1][self.elec.CANDIDATE_INDEX]] += 1
            else:
                for _, candidate in enumerate(reversed(voter)):
                    if candidate[self.elec.CANDIDATE_SCORE] > 0:
                        self.candidates[candidate[self.elec.CANDIDATE_INDEX]] += 1
                    else:
                        break

    def simulate(self):
        print("APPROVAL VOTING SYSTEM")

        self._count_votes()
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