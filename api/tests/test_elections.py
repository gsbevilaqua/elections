import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from Elections import Elections
from nose.tools import assert_equals

elec = None
elec2 = None

def setup_module(module):
    global elec, elec2
    print ("") # this is to get a newline after the dots
    print ("Setup...")
    elec = Elections(1000, [0, 0, 0, 0], 1)
    elec.reset()
    elec2 = Elections(1000, [0, 0, 0, 0, 0], 1, voter_profiles = [{"pop_percentage": 100, "scores": [10, 5, 0, -5, -10]}])
    elec2.reset()
    elec2.create_candidates()
    elec2.create_voters()
 
def teardown_module(module):
    print ("")
    print ("Teardown...")

def test_create_candidates():
    global elec
    elec.create_candidates()
    assert_equals(len(elec.candidates), 4)
    assert_equals(len(elec.votes), 4)

def test_create_voters():
    global elec
    elec.create_voters()
    assert_equals(len(elec.voters), 1000)
    elec3 = Elections(1000, [0, 0, 0, 0], 1, voter_profiles = [{"pop_percentage": 50, "scores": [-10, -5, 5, 10]}, {"pop_percentage": 50, "scores": [6, 3, 1, 0]}])
    elec3.reset()
    elec3.create_voters()
    assert_equals(len(elec3.voters), 1000)

def test_account_for_coalitions():
    global elec2
    length = len(elec2.voters)
    elec2._account_for_coalitions()
    assert_equals(len(elec2.voters), length)

def test_sort_ranks():
    global elec2
    elec2.sort_ranks()
    assert len(elec2.sorted_voters) > 0

def test_sort_candidates():
    global elec
    sor = elec.sort_candidates(elec.candidates)
    assert_equals(len(elec.candidates), len(sor))

def test_calculate_mean():
    global elec2
    assert_equals(elec2.calculate_mean([0]), (10, 1.0, False))
    assert_equals(elec2.calculate_mean([1]), (5, 1.0, False))
    assert_equals(elec2.calculate_mean([2]), (0, 0.0, False))
    assert_equals(elec2.calculate_mean([3]), (-5, 0.0, False))
    assert_equals(elec2.calculate_mean([4]), (-10, 0.0, False))

