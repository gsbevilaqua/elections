import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from Elections import Elections
from ApprovalVoting import ApprovalVoting
from nose.tools import assert_equals

elec = None
elec2 = None
avs = None
avs2 = None

def setup_module(module):
    global elec, elec2, elec3, avs, avs2
    print ("") # this is to get a newline after the dots
    print ("Setup...")
    elec = Elections(1000, [0, 0, 0, 0], 1, voter_profiles = [{"pop_percentage": 40, "scores": [10, -10, -10, -10]},
                                                              {"pop_percentage": 12, "scores": [5, -10, -10, 10]},
                                                              {"pop_percentage": 24, "scores": [-10, 6, 3, -10]},
                                                              {"pop_percentage": 24, "scores": [-10, 3, 6, -10]}])
    elec2 = Elections(1000, [0, 0, 0, 0], 1, voter_profiles = [{"pop_percentage": 40, "scores": [10, -10, -10, -10]},
                                                              {"pop_percentage": 10, "scores": [5, -10, -10, 10]},
                                                              {"pop_percentage": 26, "scores": [-10, 6, 3, -10]},
                                                              {"pop_percentage": 24, "scores": [-10, 3, 6, -10]}], tactical = 1, tactical_votes = [0.0, 0.0, 1.0, 1.0])
    elec.reset()
    elec.create_candidates()
    elec.create_voters()
    elec.sort_ranks()
    elec2.reset()
    elec2.create_candidates()
    elec2.create_voters()
    elec2.sort_ranks()
    avs = ApprovalVoting(elec)
    avs2 = ApprovalVoting(elec2)
 
def teardown_module(module):
    print ("")
    print ("Teardown...")

def test_count_votes():
    global avs
    avs._count_votes()
    avs.sorted_candidates = avs.elec.sort_candidates(avs.candidates)
    assert_equals(avs.sorted_candidates, [(3, 120),(1, 480),(2, 480),(0, 520)])

def test_count_votes_with_tactical():
    global avs2
    avs2._count_votes_with_tactical()
    avs2.sorted_candidates = avs2.elec.sort_candidates(avs2.candidates)
    assert_equals(avs2.sorted_candidates, [(3, 100),(1, 260),(0, 400),(2, 500)])