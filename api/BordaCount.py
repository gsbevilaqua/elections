import random, copy, time
from api.Elections import Elections
#from Elections import Elections # used for testing

class BordaCount:

    elec = None
    candidates = dict()
    sorted_candidates = []
    votes = dict()
    t_votes_changed = 0
    rankings_changed = dict()
    leading_candidates = []

    def __init__(self, elec):
        start_time = time.time()
        self.elec = elec
        self.votes = copy.deepcopy(elec.votes)
        if elec.seed is not None:
            random.seed(elec.seed)
        print('TBC init: ' + str(round(time.time() - start_time, 2)) + ' seg' )

    def reset(self):
        self.candidates = dict()
        self.sorted_candidates = []
        self.t_votes_changed = 0
        self.rankings_changed = dict()
        self.leading_candidates = []

    # def _apply_tactical_votes(self):
    #     print("::::::::APPLYING TACTICAL VOTES...")
    #     t_votes_changed = 0
    #     for voter_index, voter in enumerate(self.elec.sorted_voters):
    #         if random.random() < self.elec.tactical_vote_percentages[voter[-1][self.elec.CANDIDATE_INDEX]]:
    #             t_votes_changed += 1
    #             temp = []
    #             for candidate in reversed(self.elec.sorted_candidates):
    #                 if candidate[0] == voter[-1][self.elec.CANDIDATE_INDEX]:
    #                     continue
    #                 else:
    #                     temp.append((candidate[0], 0))
    #             temp.append((voter[-1][self.elec.CANDIDATE_INDEX], 10))
    #             self.rankings_changed[voter_index] = temp
		
    #     print("::::: T votes changed: ", t_votes_changed)

    def _apply_tactical_votes(self):
        print("::::::::APPLYING TACTICAL VOTES...")
        t_votes_changed = 0
        pos = set()
        for index, perc in enumerate(self.elec.tactical_vote_percentages):
            if perc > 0:
                pos.add(index)
        print("pos: ", pos)
        for candidate in self.elec.candidates:
            if candidate not in self.leading_candidates:
                for voter_index in self.votes[candidate]:
                    raised = None
                    for candidate_tuple in reversed(self.elec.sorted_voters[voter_index]):
                        if candidate_tuple[self.elec.CANDIDATE_INDEX] in self.leading_candidates:
                            if candidate_tuple[self.elec.CANDIDATE_INDEX] in pos:
                                if random.random() < self.elec.tactical_vote_percentages[candidate_tuple[self.elec.CANDIDATE_INDEX]]:
                                    # print(self.elec.sorted_voters[voter_index])
                                    ranking = [None]*self.elec.N_CANDIDATES
                                    ranking[-1] = (candidate_tuple[self.elec.CANDIDATE_INDEX], self.elec.voters[voter_index][candidate_tuple[self.elec.CANDIDATE_INDEX]])
                                    raised = candidate_tuple[self.elec.CANDIDATE_INDEX]
                                    break
                                break
                            break
                    if raised != None:
                        # print("raised: ", raised)
                        for _candidate in self.leading_candidates:
                            if _candidate != ranking[-1][0]:
                                ranking[0] = (_candidate, self.elec.voters[voter_index][_candidate])
                                buried = _candidate
                                break
                        i = 1
                        # print("buried: ", buried)
                        for candidate_tuple in self.elec.sorted_voters[voter_index]:
                            # print(i)
                            # print(candidate_tuple)
                            if candidate_tuple[self.elec.CANDIDATE_INDEX] in [raised, buried]:
                                continue
                            else:
                                ranking[i] = (candidate_tuple[self.elec.CANDIDATE_INDEX], self.elec.voters[voter_index][candidate_tuple[self.elec.CANDIDATE_INDEX]])
                                i += 1
                        self.rankings_changed[voter_index] = ranking
                        # print("new: ", ranking)
            elif candidate in pos:
                for voter_index in self.votes[candidate]:
                    if random.random() < self.elec.tactical_vote_percentages[candidate]:
                        # print(self.elec.sorted_voters[voter_index])
                        for _candidate in self.leading_candidates:
                            if _candidate != candidate:
                                ranking = [None]*self.elec.N_CANDIDATES
                                ranking[0] = (_candidate, self.elec.voters[voter_index][_candidate])
                                buried = _candidate
                                break
                        i = 1
                        # print("buried: ", buried)
                        for candidate_tuple in self.elec.sorted_voters[voter_index]:
                            # print(i)
                            # print(candidate_tuple)
                            if candidate_tuple[self.elec.CANDIDATE_INDEX] == buried:
                                continue
                            else:
                                ranking[i] = (candidate_tuple[self.elec.CANDIDATE_INDEX], self.elec.voters[voter_index][candidate_tuple[self.elec.CANDIDATE_INDEX]])
                                i += 1
                        self.rankings_changed[voter_index] = ranking
                        # print("new: ", ranking)


    def _sum_candidates_scores(self):
        for index in range(self.elec.N_CANDIDATES):
            self.candidates[index] = 0

        for voter_index, voter in enumerate(self.elec.sorted_voters):
            score = 0
            if voter_index in self.rankings_changed:
                for candidate in self.rankings_changed[voter_index]:
                    self.candidates[candidate[self.elec.CANDIDATE_INDEX]] += score
                    score += 1
            else:
                for candidate in voter:
                    self.candidates[candidate[self.elec.CANDIDATE_INDEX]] += score
                    score += 1

    # THIS FILLS 'leading_candidates' LIST: THE FIRST (N_VACANCIES + 1) CANDIDATES
    def _set_leading_candidates(self):
        for i in range(1, self.elec.N_VACANCIES + 2):
            self.leading_candidates.append(self.sorted_candidates[-i][self.elec.CANDIDATE_INDEX])
        print("leading: ", self.leading_candidates)

    def simulate(self):
        print("BORDA COUNT")
        start_time = time.time()

        self._sum_candidates_scores()
        self.sorted_candidates = self.elec.sort_candidates(self.candidates)
        if self.elec.TACTICAL_VOTING:
            self._set_leading_candidates()
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
        mean, satisfaction_rate, chose_best = self.elec.get_mean(winners = winners)

        elected = out[0][-self.elec.N_VACANCIES:]

        now = time.time()
        print('TBC duration: ' + str(round(now - start_time, 2)) + ' seg' )
        return out, mean, elected, satisfaction_rate, chose_best