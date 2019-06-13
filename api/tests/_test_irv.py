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
    elec = Elections(1000, [0, 0, 0, 0], 1, voter_profiles = [{"pop_percentage": 50, "scores": [10, -10, -10, -10,]},
                                                              {"pop_percentage": 30, "scores": [-10, 10, -10, -10,]},
                                                              {"pop_percentage": 15, "scores": [-10, -10, 10, -10,]},
                                                              {"pop_percentage": 5, "scores": [1, -10, -10, 10,]}], tactical = 1, tactical_votes = [1.0, 0.0, 0.0, 0.0])
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
    irv = InstantRunoffVoting(elec)
    irv2 = InstantRunoffVoting(elec2)
    irv3 = InstantRunoffVoting(elec3)
 
def teardown_module(module):
    print ("")
    print ("Teardown...")

def test_count_votes():
    
