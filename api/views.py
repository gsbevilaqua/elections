from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
import json

from api.FirstPastThePost import FirstPastThePost
from api.TwoRoundSystem import TwoRoundSystem
from api.InstantRunoffVoting import InstantRunoffVoting
from api.ApprovalVoting import ApprovalVoting
from api.BordaCount import BordaCount
from api.ScoreVoting import ScoreVoting
from api.BlocVote import BlocVote
from api.Elections import Elections

elec = None

def create_candidates(request):
    global elec
    print(request.body)
    n_voters = json.loads(request.body.decode('utf-8')).get('n_voters')
    n_vacancies = json.loads(request.body.decode('utf-8')).get('n_vacancies')
    candidates = json.loads(request.body.decode('utf-8')).get('candidates')
    candidates_names = json.loads(request.body.decode('utf-8')).get('candidates_names')
    tactical = json.loads(request.body.decode('utf-8')).get('tactical')
    minority = json.loads(request.body.decode('utf-8')).get('minority')
    tactical_votes = json.loads(request.body.decode('utf-8')).get('tactical_votes')
    minority_votes = json.loads(request.body.decode('utf-8')).get('minority_votes')
    coalitions = json.loads(request.body.decode('utf-8')).get('coalitions')
    voters = json.loads(request.body.decode('utf-8')).get('voters')
    seed = json.loads(request.body.decode('utf-8')).get('seed')

    if seed is not None:
        seed = int(seed)

    elec = Elections(int(n_voters), candidates, int(n_vacancies), tactical, minority, tactical_votes, minority_votes, coalitions, candidates_names, voters, seed)
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
    print(request.body)
    fptp = json.loads(request.body.decode('utf-8')).get('one_round')
    trs = json.loads(request.body.decode('utf-8')).get('two_rounds')
    irv = json.loads(request.body.decode('utf-8')).get('irv')
    avs = json.loads(request.body.decode('utf-8')).get('avs')
    tbc = json.loads(request.body.decode('utf-8')).get('tbc')
    svs = json.loads(request.body.decode('utf-8')).get('svs')
    bvs = json.loads(request.body.decode('utf-8')).get('bvs')

    status = "null"
    status1 = "null"
    status2 = "null"
    status3 = "null"
    status4 = "null"
    status5 = "null"
    status6 = "null"

    if(fptp):
        fptp = FirstPastThePost(elec)
        fptp.reset()
        status = fptp.simulate()
    if(trs):
        trs = TwoRoundSystem(elec)
        trs.reset()
        status1 = trs.simulate()
    if(irv):
        irv = InstantRunoffVoting(elec)
        irv.reset()
        status2 = irv.simulate()
    if(avs):
        avs = ApprovalVoting(elec)
        avs.reset()
        status6 = avs.simulate()        
    if(tbc):
        tbc = BordaCount(elec)
        tbc.reset()
        status4 = tbc.simulate()
    if(svs):
        svs = ScoreVoting(elec)
        svs.reset()
        status3 = svs.simulate()        
    if(bvs):
        bvs = BlocVote(elec)
        bvs.reset()
        status5 = bvs.simulate()

    return JsonResponse({
        'status': status,
        'status1': status1,
        'status2': status2,
        'status3': status3,
        'status4': status4,
        'status5': status5,
        'status6': status6
    })

def direct_results(request):
    global elec
    print(request.body)
    n_voters = json.loads(request.body.decode('utf-8')).get('n_voters')
    n_vacancies = json.loads(request.body.decode('utf-8')).get('n_vacancies')
    candidates = json.loads(request.body.decode('utf-8')).get('candidates')
    candidates_names = json.loads(request.body.decode('utf-8')).get('candidates_names')
    tactical = json.loads(request.body.decode('utf-8')).get('tactical')
    minority = json.loads(request.body.decode('utf-8')).get('minority')
    tactical_votes = json.loads(request.body.decode('utf-8')).get('tactical_votes')
    minority_votes = json.loads(request.body.decode('utf-8')).get('minority_votes')
    coalitions = json.loads(request.body.decode('utf-8')).get('coalitions')
    voters = json.loads(request.body.decode('utf-8')).get('voters')
    seed = json.loads(request.body.decode('utf-8')).get('seed')
    fptp = json.loads(request.body.decode('utf-8')).get('one_round')
    trs = json.loads(request.body.decode('utf-8')).get('two_rounds')
    irv = json.loads(request.body.decode('utf-8')).get('irv')
    avs = json.loads(request.body.decode('utf-8')).get('avs')
    tbc = json.loads(request.body.decode('utf-8')).get('tbc')
    svs = json.loads(request.body.decode('utf-8')).get('svs')
    bvs = json.loads(request.body.decode('utf-8')).get('bvs')

    print("DEWDEWDWE", seed)

    elec = Elections(int(n_voters), candidates, int(n_vacancies), tactical, minority, tactical_votes, minority_votes, coalitions, candidates_names, voters, int(seed))
    elec.reset()
    elec.create_candidates()
    elec.create_voters()
    elec.sort_ranks()

    status = "null"
    status1 = "null"
    status2 = "null"
    status3 = "null"
    status4 = "null"
    status5 = "null"
    status6 = "null"

    if(fptp):
        fptp = FirstPastThePost(elec)
        fptp.reset()
        status = fptp.simulate()
    if(trs):
        trs = TwoRoundSystem(elec)
        trs.reset()
        status1 = trs.simulate()
    if(irv):
        irv = InstantRunoffVoting(elec)
        irv.reset()
        status2 = irv.simulate()
    if(avs):
        avs = ApprovalVoting(elec)
        avs.reset()
        status6 = avs.simulate()        
    if(tbc):
        tbc = BordaCount(elec)
        tbc.reset()
        status4 = tbc.simulate()
    if(svs):
        svs = ScoreVoting(elec)
        svs.reset()
        status3 = svs.simulate()        
    if(bvs):
        bvs = BlocVote(elec)
        bvs.reset()
        status5 = bvs.simulate()

    return JsonResponse({
        'status': status,
        'status1': status1,
        'status2': status2,
        'status3': status3,
        'status4': status4,
        'status5': status5,
        'status6': status6
    })    