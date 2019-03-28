import { SET_TWO_ROUNDS, SET_IRV, SET_NUMBER_CANDIDATES, SET_NUMBER_VOTERS, SET_NUMBER_VACANCIES, ADD_CANDIDATE, DELETE_CANDIDATE, SET_NAME, SET_FAME, RESET } from '../actions/types.js'

const initial_state = {
    two_rounds: false,
    irv: false,
    n_voters: 1000,
    n_vacancies: 1,
    candidates: [],
    candidates_names: []
}

export default function(state = initial_state, action) {
    switch(action.type) {
        case SET_TWO_ROUNDS:
            return {
                ...state,
                two_rounds: !state.two_rounds
            }
        case SET_IRV:
            return {
                ...state,
                irv: !state.irv
            }
        case SET_NUMBER_CANDIDATES:
            return {
                ...state,
                candidates: action.payload.fames,
                candidates_names: action.payload.names
            }
        case SET_NUMBER_VOTERS:
            return{
                ...state,
                n_voters: action.payload
            }
        case SET_NUMBER_VACANCIES:
            return{
                ...state,
                n_vacancies: action.payload
            }            
        case ADD_CANDIDATE:
            return{
                ...state,
                candidates: [...state.candidates, action.payload.fame],
                candidates_names: [...state.candidates_names, action.payload.name]
            }
        case DELETE_CANDIDATE:
            return{
                ...state,
                candidates: [...state.candidates.slice(0, action.payload), ...state.candidates.slice(action.payload + 1)],
                candidates_names: [...state.candidates.slice(0, action.payload), ...state.candidates.slice(action.payload + 1)]
            }
        case SET_NAME:
            return{
                ...state,
                candidates_names: [...state.candidates.slice(0, action.payload[0]), action.payload[1], ...state.candidates.slice(action.payload[0] + 1)]
            }
        case SET_FAME:
            return{
                ...state,
                candidates: [...state.candidates.slice(0, action.payload[0]), action.payload[1], ...state.candidates.slice(action.payload[0] + 1)]
            }
        case RESET:
            return{
                two_rounds: false,
                irv: false,
                n_voters: 1000,
                n_vacancies: 1,
                candidates: [],
                candidates_names: []
            }                       
        default:
            return state;
    }
}