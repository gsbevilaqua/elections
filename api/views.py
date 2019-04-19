from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
import json

from api.OneRoundSystem import OneRoundSystem
from api.TwoRoundSystem import TwoRoundSystem
from api.InstantRunoffVoting import InstantRunoffVoting
from api.ScoreBased import ScoreBased
from api.FixedScoreBased import FixedScoreBased
from api.MultipleVotesCast import MultipleVotesCast
from api.Elections import Elections

elec = None

def create_candidates(request):
    global elec
    n_voters = json.loads(request.body.decode('utf-8')).get('n_voters')
    n_vacancies = json.loads(request.body.decode('utf-8')).get('n_vacancies')
    candidates = json.loads(request.body.decode('utf-8')).get('candidates')
    candidates_names = json.loads(request.body.decode('utf-8')).get('candidates_names')
    tactical = json.loads(request.body.decode('utf-8')).get('tactical')
    minority = json.loads(request.body.decode('utf-8')).get('minority')
    tactical_votes = json.loads(request.body.decode('utf-8')).get('tactical_votes')
    minority_votes = json.loads(request.body.decode('utf-8')).get('minority_votes')
    coalitions = json.loads(request.body.decode('utf-8')).get('coalitions')

    elec = Elections(int(n_voters), candidates, n_vacancies, tactical, minority, tactical_votes, minority_votes, coalitions, candidates_names)
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
    one_round = json.loads(request.body.decode('utf-8')).get('one_round')
    two_rounds = json.loads(request.body.decode('utf-8')).get('two_rounds')
    irv = json.loads(request.body.decode('utf-8')).get('irv')
    scores = json.loads(request.body.decode('utf-8')).get('sbs')
    fsb = json.loads(request.body.decode('utf-8')).get('fsb')
    mvc = json.loads(request.body.decode('utf-8')).get('mvc')

    status = "null"
    status1 = "null"
    status2 = "null"
    status3 = "null"
    status4 = "null"
    status5 = "null"

    if(one_round):
        ors = OneRoundSystem(elec)
        status = ors.simulate()
    if(two_rounds):
        trs = TwoRoundSystem(elec)
        status1 = trs.simulate()
    if(irv):
        irv = InstantRunoffVoting(elec)
        status2 = irv.simulate()
    if(scores):
        scores = ScoreBased(elec)
        status3 = scores.simulate()
    if(fsb):
        fsb = FixedScoreBased(elec)
        status4 = fsb.simulate()
    if(mvc):
        mvc = MultipleVotesCast(elec)
        status5 = mvc.simulate()

    return JsonResponse({
        'status': status,
        'status1': status1,
        'status2': status2,
        'status3': status3,
        'status4': status4,
        'status5': status5
    })