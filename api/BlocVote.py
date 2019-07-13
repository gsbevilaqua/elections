import copy, time
from api.Elections import Elections
#from Elections import Elections # used for testing

class BlocVote:

    elec = None
    candidates = dict()
    sorted_candidates = []

    def __init__(self, elec):
        start_time = time.time()
        self.elec = elec
        print('BVS init: ' + str(round(time.time() - start_time, 2)) + ' seg' )

    def reset(self):
        self.candidates = dict()
        self.sorted_candidates = []

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
        print("BLOC VOTE")
        start_time = time.time()

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
        mean, satisfaction_rate, chose_best = self.elec.get_mean(winners = winners)

        elected = out[0][-self.elec.N_VACANCIES:]

        now = time.time()
        print('BVS duration: ' + str(round(now - start_time, 2)) + ' seg' )
        return out, mean, elected, satisfaction_rate