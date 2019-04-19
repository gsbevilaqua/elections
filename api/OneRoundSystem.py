from api.Elections import Elections
#from Elections import Elections

class OneRoundSystem:

    elec = None
    sorted_candidates = []

    def __init__(self, elec):
        self.elec = elec
        self.sorted_candidates = self.elec.sort_candidates(self.elec.candidates)

    def simulate(self):
        print("ONE ROUND SYSTEM")

        print(self.elec.candidates_names)

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
        mean, satisfaction_rate = self.elec.calculate_mean(winners = winners)

        elected = out[0][-self.elec.N_VACANCIES:]

        return out, mean, elected, satisfaction_rate