import { SET_ONE_ROUND, SET_TWO_ROUNDS, SET_IRV, SET_AVS, SET_TBC, SET_SVS, SET_BVS, SET_NUMBER_CANDIDATES, SET_NUMBER_VOTERS, SET_NUMBER_VACANCIES, ADD_CANDIDATE, DELETE_CANDIDATE, SET_NAME, SET_FAME, RESET, SET_TACTICAL_PERC, SET_MINORITY_PERC, ADD_COALITION, ADD_CANDIDATE_TO_COALITION, DELETE_COALITION, SET_CANDIDATE, SET_NUMBER_PROFILES, ADD_VOTER, DELETE_VOTER, SET_CANDIDATE_SCORE, SET_PROFILE_NAME, SET_PROFILE_PERC } from './types';

export const setOneRound = (val) => dispatch => {
    dispatch({
        type: SET_ONE_ROUND
    });
}

export const setTwoRounds = (val) => dispatch => {
    dispatch({
        type: SET_TWO_ROUNDS
    });
}

export const setIrv = (val) => dispatch => {
    dispatch({
        type: SET_IRV
    });
}

export const setAvs = (val) => dispatch => {
    dispatch({
        type: SET_AVS
    });
}

export const setTbc = (val) => dispatch => {
    dispatch({
        type: SET_TBC
    });
}

export const setSvs = (val) => dispatch => {
    dispatch({
        type: SET_SVS
    });
}

export const setBvs = (val) => dispatch => {
    dispatch({
        type: SET_BVS
    });
}

export const setNCandidates = (val) => dispatch => {
    let candidates_array = [];
    let candidates_names_array = [];
    let tactical_votes_array = [];
    let minority_votes_array = [];
    let ava = [];

    for (let index = 0; index < val; index++) {
        candidates_array.push(0);
        candidates_names_array.push("Candidate " + index);
        tactical_votes_array.push(0.0);
        minority_votes_array.push(0.0);
        ava.push({"value": index, "label": "Candidate " + index});
    }

    dispatch({
        type: SET_NUMBER_CANDIDATES,
        payload: { fames: candidates_array, names: candidates_names_array, tacts: tactical_votes_array, minos: minority_votes_array, ava: ava }
    });
}

export const setNVoters = (val) => dispatch => {
    if(val == '' || val == null){
        val = 1000;
    }

    dispatch({
        type: SET_NUMBER_VOTERS, 
        payload: parseInt(val)
    });
}

export const setNVacancies = (val) => dispatch => {
    if(val == '' || val == null){
        val = 1;
    }

    dispatch({
        type: SET_NUMBER_VACANCIES, 
        payload: parseInt(val)
    });
}

export const addCandidate = (fame, name, tact, mino, index) => dispatch => {
    dispatch({
        type: ADD_CANDIDATE, 
        payload: { fame: fame, name: name, tact: tact, mino: mino, ava: {"value": index, "label": "Candidate " + index} }
    });
}

export const deleteCandidate = (val) => dispatch => {
    dispatch({
        type: DELETE_CANDIDATE,
        payload: val
    });
}

export const setName = (index, name) => dispatch => {
    dispatch({
        type: SET_NAME,
        payload: {index: index, name: name, ava: {"value": index, "label": name}}
    });
}

export const setFame = (index, fame) => dispatch => {
    dispatch({
        type: SET_FAME,
        payload: {index: index, fame: fame}
    });
}

export const fullReset = () => dispatch => {
    dispatch({type: RESET});
}

export const setTactical = (index, tact) => dispatch => {
    let val = parseFloat(tact);
    dispatch({
        type: SET_TACTICAL_PERC,
        payload: [index, val]
    });
}

export const setMinority = (index, mino) => dispatch => {
    let val = parseFloat(mino);
    dispatch({
        type: SET_MINORITY_PERC,
        payload: [index, val]
    });
}

export const addCoalition = () => dispatch => {
    dispatch({
        type: ADD_COALITION
    });
}

export const deleteCoalition = (index) => dispatch => {
    dispatch({
        type: DELETE_COALITION,
        payload: index
    });
}

export const addCandidateToCoalition = (index, vec) => dispatch => {
    vec.push("NO CANDIDATE");
    dispatch({
        type: ADD_CANDIDATE_TO_COALITION,
        payload: [index, vec]
    });
}

export const setCandidate = (index, index2, val) => dispatch => {
    dispatch({
        type: SET_CANDIDATE,
        payload: [index, index2, val]
    });
}

export const setNProfiles = (val) => dispatch => {
    let voters = []
    
    for (let index = 0; index < val; index++) {
        voters.push({pop_percentage: 0.0, name: "Voter Profile " + index, scores: []})
    }

    dispatch({
        type: SET_NUMBER_PROFILES,
        payload: voters
    });
}

export const addVoter = (pop, name, scores) => dispatch => {
    dispatch({
        type: ADD_VOTER,
        payload: { pop_percentage: pop, name: name, scores: scores }
    });
}

export const deleteVoter = (val) => dispatch => {
    dispatch({
        type: DELETE_VOTER,
        payload: val
    });
}

export const setCandidateScore = (val, profile_index, candidate_index) => dispatch => {
    dispatch({
        type: SET_CANDIDATE_SCORE,
        payload: { val: val, profile_index: profile_index, candidate_index: candidate_index }
    });
}

export const setProfileName = (index, val) => dispatch => {
    dispatch({
        type: SET_PROFILE_NAME,
        payload: {index: index, val: val}
    });
}

export const setProfilePerc = (index, val) => dispatch => {
    dispatch({
        type: SET_PROFILE_PERC,
        payload: {index: index, val: val}
    });
}