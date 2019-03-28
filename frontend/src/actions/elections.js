import { SET_TWO_ROUNDS, SET_IRV, SET_NUMBER_CANDIDATES, SET_NUMBER_VOTERS, SET_NUMBER_VACANCIES, ADD_CANDIDATE, DELETE_CANDIDATE, SET_NAME, SET_FAME, RESET } from './types';

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

export const setNCandidates = (val) => dispatch => {
    let candidates_array = [];
    let candidates_names_array = [];
    for (let index = 0; index < val; index++) {
        candidates_array.push(0);
        candidates_names_array.push("Candidate " + index);
    }

    dispatch({
        type: SET_NUMBER_CANDIDATES,
        payload: { fames: candidates_array, names: candidates_names_array }
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

export const addCandidate = (fame, name) => dispatch => {
    dispatch({
        type: ADD_CANDIDATE, 
        payload: { fame: fame, name: name }
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