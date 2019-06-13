import random, copy, time
from api.Elections import Elections
#from Elections import Elections # used for testing

class ApprovalVoting:

    elec = None
    candidates = dict()
    sorted_candidates = []

    def __init__(self, elec):
        start_time = time.time()
        self.elec = elec
        print('AVS init: ' + str(round(time.time() - start_time, 2)) + ' seg' )

    def _count_votes_with_tactical(self):
        for index in range(self.elec.N_CANDIDATES):
            self.candidates[index] = 0

        t_votes_changed = 0
        for voter in self.elec.sorted_voters:
            if random.random() < self.elec.tactical_vote_percentages[voter[-1][self.elec.CANDIDATE_INDEX]]:
                t_votes_changed += 1
                self.candidates[voter[-1][self.elec.CANDIDATE_INDEX]] += 1
            else:
                for candidate in reversed(voter):
                    if candidate[self.elec.CANDIDATE_SCORE] > 0:
                        self.candidates[candidate[self.elec.CANDIDATE_INDEX]] += 1
                    else:
                        break

    def _count_votes(self):
        for index in range(self.elec.N_CANDIDATES):
            self.candidates[index] = 0

        t_votes_changed = 0
        for voter in self.elec.sorted_voters:
            for candidate in reversed(voter):
                if candidate[self.elec.CANDIDATE_SCORE] > 0:
                    self.candidates[candidate[self.elec.CANDIDATE_INDEX]] += 1
                else:
                    break

    def simulate(self):
        print("APPROVAL VOTING SYSTEM")
        start_time = time.time()
        
        if self.elec.TACTICAL_VOTING:
            self._count_votes_with_tactical()
        else:
            self._count_votes()
        self.sorted_candidates = self.elec.sort_candidates(self.candidates)

        out = [[], []]
        print(self.elec.candidates_names)
        print(self.sorted_candidates)
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

        now = time.time()
        print('AVS duration: ' + str(round(now - start_time, 2)) + ' seg' )
        return out, mean, elected, satisfaction_rate