import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from Elections import Elections
from TwoRoundSystem import TwoRoundSystem
from nose.tools import assert_equals

elec = None
elec2 = None
elec3 = None
trs = None
trs2 = None
trs3 = None

def setup_module(module):
    global elec, elec2, elec3, trs, trs2, trs3
    print ("") # this is to get a newline after the dots
    print ("Setup...")
    elec = Elections(1000, [0, 0, 0, 0], 1, voter_profiles = [{"pop_percentage": 50, "scores": [10, -10, -10, -10]},
                                                              {"pop_percentage": 30, "scores": [-10, 10, -10, -10]},
                                                              {"pop_percentage": 15, "scores": [-10, -10, 10, -10]},
                                                              {"pop_percentage": 5, "scores": [1, -10, -10, 10]}], tactical = 1, tactical_votes = [1.0, 0.0, 0.0, 0.0])
    elec2 = Elections(1000, [0, 0, 0, 0], 2, voter_profiles = [{"pop_percentage": 100, "scores": [10, -10, -10, -10]}], tactical = 1)
    elec3 = Elections(1000, [0, 0, 0, 0, 0, 0, 0], 5, voter_profiles = [{"pop_percentage": 55, "scores": [10, 5, 4, 3, 8, 1, -10]},{"pop_percentage": 45, "scores": [-10, -10, -10, -10, -10, -10, 0]}], minority = 1, minority_votes = [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0])
    elec.reset()
    elec.create_candidates()
    elec.create_voters()
    elec.sort_ranks()
    elec2.reset()
    elec2.create_candidates()
    elec2.create_voters()
    elec2.sort_ranks()
    elec3.reset()
    elec3.create_candidates()
    elec3.create_voters()
    elec3.sort_ranks()
    trs = TwoRoundSystem(elec)
    trs2 = TwoRoundSystem(elec2)
    trs3 = TwoRoundSystem(elec3)
 
def teardown_module(module):
    print ("")
    print ("Teardown...")

def test_set_leading_candidates():
    global trs, trs2, trs3
    assert_equals(len(trs.elec.leading_candidates), 3)
    assert_equals(len(trs2.elec.leading_candidates), 3)
    assert_equals(len(trs3.elec.leading_candidates), 6)

def test_count_tactical_votes():
    global trs, trs2
    trs._count_tactical_votes()
    trs2._count_tactical_votes()
    assert_equals(trs.t_votes_changed, 50)
    assert_equals(trs2.t_votes_changed, 0)

def test_count_minority_votes():
    global trs3
    trs3._count_minority_votes()
    assert_equals(trs3.m_votes_changed, 550)