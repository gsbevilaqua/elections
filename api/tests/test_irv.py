import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from Elections import Elections
from InstantRunoffVoting import InstantRunoffVoting
from nose.tools import assert_equals

elec = None
elec2 = None
elec3 = None
irv = None
irv2 = None
irv3 = None

def setup_module(module):
    global elec, elec2, elec3, irv, irv2, irv3
    print ("") # this is to get a newline after the dots
    print ("Setup...")
    elec = Elections(1000, [0, 0, 0, 0], 1, voter_profiles = [{"pop_percentage": 40, "scores": [10, -10, -10, -10,]},
                                                              {"pop_percentage": 12, "scores": [5, -10, -10, 10,]},
                                                              {"pop_percentage": 24, "scores": [-10, 6, 3, -10,]},
                                                              {"pop_percentage": 24, "scores": [-10, 3, 6, -10,]}])
    elec2 = Elections(1000, [0, 0, 0, 0], 1, voter_profiles = [{"pop_percentage": 40, "scores": [10, -10, -10, -10,]},
                                                              {"pop_percentage": 10, "scores": [5, -10, -10, 10,]},
                                                              {"pop_percentage": 26, "scores": [-10, 6, 3, -10,]},
                                                              {"pop_percentage": 24, "scores": [-10, 3, 6, -10,]}])
    #elec3 = Elections(1000, [0, 0, 0, 0], 1, voter_profiles = [{"pop_percentage": 40, "scores": [10, -10, -10, -10,]},
    #                                                          {"pop_percentage": 12, "scores": [5, -10, -10, 10,]},
    #                                                          {"pop_percentage": 24, "scores": [-10, 6, 3, -10,]},
    #                                                          {"pop_percentage": 24, "scores": [-10, 3, 6, -10,]}])
    elec.reset()
    elec.create_candidates()
    elec.create_voters()
    elec.sort_ranks()
    elec2.reset()
    elec2.create_candidates()
    elec2.create_voters()
    elec2.sort_ranks()
    # elec3.reset()
    # elec3.create_candidates()
    # elec3.create_voters()
    # elec3.sort_ranks()
    irv = InstantRunoffVoting(elec)
    irv2 = InstantRunoffVoting(elec2)
    # irv3 = InstantRunoffVoting(elec3)
 
def teardown_module(module):
    print ("")
    print ("Teardown...")

def test_count_votes():
    global irv, irv2
    irv.sorted_candidates = irv.elec.sort_candidates(irv.candidates)
    irv2.sorted_candidates = irv2.elec.sort_candidates(irv2.candidates)
    irv._count_votes(0)
    ret = irv._count_votes(1)
    assert_equals(ret, 1)
    irv2._count_votes(0)
    ret = irv2._count_votes(1)
    assert_equals(ret, 0)
    ret = irv2._count_votes(2)
    assert_equals(ret, 2)