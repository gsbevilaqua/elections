import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from Elections import Elections
from BordaCount import BordaCount
from nose.tools import assert_equals

elec = None
elec2 = None
tbc = None
tbc2 = None

def setup_module(module):
    global elec, elec2, elec3, tbc, tbc2
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
    tbc = BordaCount(elec)
    tbc2 = BordaCount(elec2)
 
def teardown_module(module):
    print ("")
    print ("Teardown...")

def test_sum_candidates_scores():
    global tbc
    tbc._sum_candidates_scores()
    tbc.sorted_candidates = tbc.elec.sort_candidates(tbc.candidates)
    assert_equals(tbc.sorted_candidates, [(1, 1200),(3, 1400),(0, 1680),(2, 1720)])

def test_apply_tactical_votes():
    global tbc2
    tbc2._apply_tactical_votes()
    tbc2._sum_candidates_scores()
    tbc2.sorted_candidates = tbc2.elec.sort_candidates(tbc2.candidates)
    assert_equals(tbc2.sorted_candidates, [(1, 1120),(0, 1200),(2, 1840),(3, 1840)])