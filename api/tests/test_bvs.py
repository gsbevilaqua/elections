import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from Elections import Elections
from BlocVote import BlocVote
from nose.tools import assert_equals

elec = None
elec2 = None
bvs = None
bvs2 = None

def setup_module(module):
    global elec, elec2, elec3, bvs, bvs2
    print ("") # this is to get a newline after the dots
    print ("Setup...")
    elec = Elections(1000, [0, 0, 0, 0], 2, voter_profiles = [{"pop_percentage": 40, "scores": [10, -10, -9, -8]},
                                                              {"pop_percentage": 12, "scores": [5, -10, -9, 10]},
                                                              {"pop_percentage": 24, "scores": [-10, 6, 3, -9]},
                                                              {"pop_percentage": 24, "scores": [-9, 3, 6, -10]}])
    elec2 = Elections(1000, [0, 0, 0, 0], 3, voter_profiles = [{"pop_percentage": 40, "scores": [10, -10, -9, -8]},
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
    bvs = BlocVote(elec)
    bvs2 = BlocVote(elec2)
 
def teardown_module(module):
    print ("")
    print ("Teardown...")

def test_count_votes():
    global bvs, bvs2
    bvs._count_votes()
    bvs.sorted_candidates = bvs.elec.sort_candidates(bvs.candidates)
    assert_equals(bvs.sorted_candidates, [(1, 480),(2, 480),(0, 520),(3, 520)])
    bvs2._count_votes()
    bvs2.sorted_candidates = bvs2.elec.sort_candidates(bvs2.candidates)
    assert_equals(bvs2.sorted_candidates, [(1, 500),(0, 740),(3, 760),(2, 1000)])