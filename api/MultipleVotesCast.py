import random, copy
from api.Elections import Elections
#from Elections import Elections

class MultipleVotesCast:

    elec = None
    candidates = dict()
    sorted_candidates = []

    def __init__(self, elec):
        self.elec = elec

    def _count_votes(self):
        for index in range(self.elec.N_CANDIDATES):
            self.candidates[index] = 0

        for voter in self.elec.sorted_voters:
            votes = self.elec.N_VACANCIES
            for candidate in reversed(voter):
                if votes == 0:
                    break
                self.candidates[candidate[self.elec.CANDIDATE_INDEX]] += 1
                votes -= 1

    def simulate(self):
        print("MULTIPLE VOTES CAST SYSTEM")

        self._count_votes()
        self.sorted_candidates = self.elec.sort_candidates(self.candidates)

        out = [[], []]
        for candidate in self.sorted_candidates:
            out[0].append(self.elec.candidates_names[candidate[self.elec.CANDIDATE_INDEX]])
            out[1].append(candidate[self.elec.CANDIDATE_SCORE])
        
        mean, satisfaction_rate = self.elec.calculate_mean(self.sorted_candidates[-1][self.elec.CANDIDATE_INDEX])

        elected = out[0][-self.elec.N_VACANCIES:]

        return out, mean, elected, satisfaction_rate