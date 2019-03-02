import { SET_TWO_ROUNDS, SET_IRV, SET_NUMBER_VOTERS, ADD_CANDIDATE, DELETE_CANDIDATE, SET_FAME } from './types';

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

export const setNVoters = (val) => dispatch => {
    dispatch({
        type: SET_NUMBER_VOTERS, 
        payload: parseInt(val)
    });
}

export const addCandidate = (val) => dispatch => {
    dispatch({
        type: ADD_CANDIDATE, 
        payload: val
    });
}

export const deleteCandidate = (val) => dispatch => {
    dispatch({
        type: DELETE_CANDIDATE,
        payload: val
    });
}

export const setFame = (index, fame) => dispatch => {
    dispatch({
        type: SET_FAME,
        payload: [index, fame]
    });
}