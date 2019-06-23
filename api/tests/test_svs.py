import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from Elections import Elections
from ScoreVoting import ScoreVoting
from nose.tools import assert_equals

elec = None
elec2 = None
svs = None
svs2 = None

def setup_module(module):
    global elec, elec2, elec3, svs, svs2
    print ("") # this is to get a newline after the dots
    print ("Setup...")
    elec = Elections(1000, [0, 0, 0, 0], 1, voter_profiles = [{"pop_percentage": 40, "scores": [10, -10, -9, -8]},
                                                              {"pop_percentage": 12, "scores": [5, -10, -9, 10]},
                                                              {"pop_percentage": 24, "scores": [-10, 6, 3, -9]},
                                                              {"pop_percentage": 24, "scores": [-9, 3, 6, -10]}])
    elec2 = Elections(1000, [0, 0, 0, 0], 1, voter_profiles = [{"pop_percentage": 40, "scores": [10, -10, -9, -8]},
                                                              {"pop_percentage": 10, "scores": [5, -10, -9, 10]},
                                                              {"pop_percentage": 26, "scores": [-10, 6, 3, -9]},
                                                              {"pop_percentage": 24, "scores": [-9, 3, 6, -10]}], tactical = 1, tactical_votes = [0.0, 0.0, 1.0, 1.0])
    elec.reset()
    elec.create_candidates()
    elec.create_voters()
    elec.sort_ranks()
    elec2.reset()
    elec2.create_candidates()
    elec2.create_voters()
    elec2.sort_ranks()
    svs = ScoreVoting(elec)
    svs2 = ScoreVoting(elec2)
 
def teardown_module(module):
    print ("")
    print ("Teardown...")

def test_sum_candidates_scores():
    global svs
    svs._sum_candidates_scores()
    svs.sorted_candidates = svs.elec.sort_candidates(svs.candidates)
    assert_equals(svs.sorted_candidates, [(3, -6560),(1, -3040),(2, -2520),(0, 40)])

def test_apply_tactical_votes():
    global svs2
    svs2._apply_tactical_votes()
    svs2._sum_candidates_scores()
    svs2.sorted_candidates = svs2.elec.sort_candidates(svs2.candidates)
    assert_equals(svs2.sorted_candidates, [(3, -6940),(1, -5840),(0, -2000),(2, -1420)])