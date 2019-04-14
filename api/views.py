from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
import json

from api.TwoRoundSystem import TwoRoundSystem
from api.InstantRunoffVoting import InstantRunoffVoting
from api.Elections import Elections

elec = None

def create_candidates(request):
    global elec
    n_voters = json.loads(request.body.decode('utf-8')).get('n_voters')
    n_vacancies = json.loads(request.body.decode('utf-8')).get('n_vacancies')
    candidates = json.loads(request.body.decode('utf-8')).get('candidates')
    candidates_names = json.loads(request.body.decode('utf-8')).get('candidates_names')
    tactical_votes = json.loads(request.body.decode('utf-8')).get('tactical_votes')
    minority_votes = json.loads(request.body.decode('utf-8')).get('minority_votes')

    elec = Elections(int(n_voters), candidates, n_vacancies, tactical_votes, minority_votes, candidates_names)
    elec.reset()
    elec.create_candidates()

    return JsonResponse({
        'status': True
    })


def create_voters(request):
    global elec
    elec.create_voters()
    return JsonResponse({
        'status': True
    })

def sort_ranks(request):
    global elec
    elec.sort_ranks()
    return JsonResponse({
        'status': True
    })

def get_results(request):
    global elec
    two_rounds = json.loads(request.body.decode('utf-8')).get('two_rounds')
    irv = json.loads(request.body.decode('utf-8')).get('irv')

    status1 = "null"
    status2 = "null"

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