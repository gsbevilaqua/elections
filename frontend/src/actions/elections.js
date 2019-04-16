import { SET_TWO_ROUNDS, SET_IRV, SET_SBS, SET_NUMBER_CANDIDATES, SET_NUMBER_VOTERS, SET_NUMBER_VACANCIES, ADD_CANDIDATE, DELETE_CANDIDATE, SET_NAME, SET_FAME, RESET, SET_TACTICAL_PERC, SET_MINORITY_PERC } from './types';

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

export const setSbs = (val) => dispatch => {
    dispatch({
        type: SET_SBS
    });
}

export const setNCandidates = (val) => dispatch => {
    let candidates_array = [];
    let candidates_names_array = [];
    let tactical_votes_array = [];
    let minority_votes_array = [];
    for (let index = 0; index < val; index++) {
        candidates_array.push(0);
        candidates_names_array.push("Candidate " + index);
        tactical_votes_array.push(0.0);
        minority_votes_array.push(0.0);
    }

    dispatch({
        type: SET_NUMBER_CANDIDATES,
        payload: { fames: candidates_array, names: candidates_names_array, tacts: tactical_votes_array, minos: minority_votes_array }
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

export const addCandidate = (fame, name, tact, mino) => dispatch => {
    dispatch({
        type: ADD_CANDIDATE, 
        payload: { fame: fame, name: name, tact: tact, mino: mino }
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
        payload: [index, name]
    });
}

export const setFame = (index, fame) => dispatch => {
    dispatch({
        type: SET_FAME,
        payload: [index, fame]
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