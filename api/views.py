from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
import json

from api.TwoRoundSystem import TwoRoundSystem
from api.InstantRunoffVoting import InstantRunoffVoting

def get_results(request):
    two_rounds = json.loads(request.body.decode('utf-8')).get('two_rounds')
    irv = json.loads(request.body.decode('utf-8')).get('irv')
    n_voters = json.loads(request.body.decode('utf-8')).get('n_voters')
    candidates = json.loads(request.body.decode('utf-8')).get('candidates')

    status1 = "null"
    status2 = "null"

    if(two_rounds):
        trs = TwoRoundSystem(int(n_voters), len(candidates), candidates)
        status1 = trs.simulate()
    if(irv):
        irv = InstantRunoffVoting(int(n_voters), len(candidates), candidates)
        status2 = irv.simulate()

    return JsonResponse({
        'status1': status1,
        'status2': status2
    })