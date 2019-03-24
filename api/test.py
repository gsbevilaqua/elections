from Elections import Elections
from TwoRoundSystem import TwoRoundSystem
from InstantRunoffVoting import InstantRunoffVoting

two_rounds = True
instant_runoff = True

elec = Elections(1000000, [0,0,0,0])
elec.reset()
elec.initialize()

if(two_rounds):
    trs = TwoRoundSystem(elec)
    status1 = trs.simulate()
if(instant_runoff):
    irv = InstantRunoffVoting(elec)
    status2 = irv.simulate()