from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
import json

from api.TwoRoundSystem import TwoRoundSystem
from api.InstantRunoffVoting import InstantRunoffVoting
from api.Elections import Elections

def get_results(request):
    two_rounds = json.loads(request.body.decode('utf-8')).get('two_rounds')
    irv = json.loads(request.body.decode('utf-8')).get('irv')
    n_voters = json.loads(request.body.decode('utf-8')).get('n_voters')
    candidates = json.loads(request.body.decode('utf-8')).get('candidates')

    status1 = "null"
    status2 = "null"

    elec = Elections(int(n_voters), candidates)
    elec.reset()
    elec.initialize()

    if(two_rounds):
        trs = TwoRoundSystem(elec)
        status1 = trs.simulate()
    if(irv):
        irv = InstantRunoffVoting(elec)
        status2 = irv.simulate()

    return JsonResponse({
        'status1': status1,
        'status2': status2
    })