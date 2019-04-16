import { SET_TWO_ROUNDS, SET_IRV, SET_SBS, SET_NUMBER_CANDIDATES, SET_NUMBER_VOTERS, SET_NUMBER_VACANCIES, ADD_CANDIDATE, DELETE_CANDIDATE, SET_NAME, SET_FAME, RESET, SET_TACTICAL_PERC, SET_MINORITY_PERC } from '../actions/types.js'

const initial_state = {
    two_rounds: false,
    irv: false,
    sbs: false,
    n_voters: 1000,
    n_vacancies: 1,
    candidates: [],
    candidates_names: [],
    tactical_votes: [],
    minority_votes: []
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
        case SET_SBS:
            return {
                ...state,
                sbs: !state.sbs
            }            
        case SET_NUMBER_CANDIDATES:
            return {
                ...state,
                candidates: action.payload.fames,
                candidates_names: action.payload.names,
                tactical_votes: action.payload.tacts,
                minority_votes: action.payload.minos
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
                candidates_names: [...state.candidates_names, action.payload.name],
                tactical_votes: [...state.tactical_votes, action.payload.tact],
                minority_votes: [...state.minority_votes, action.payload.mino]
            }
        case DELETE_CANDIDATE:
            return{
                ...state,
                candidates: [...state.candidates.slice(0, action.payload), ...state.candidates.slice(action.payload + 1)],
                candidates_names: [...state.candidates_names.slice(0, action.payload), ...state.candidates_names.slice(action.payload + 1)],
                tactical_votes: [...state.tactical_votes.slice(0, action.payload), ...state.tactical_votes.slice(action.payload + 1)],
                minority_votes: [...state.minority_votes.slice(0, action.payload), ...state.minority_votes.slice(action.payload + 1)]
            }
        case SET_NAME:
            return{
                ...state,
                candidates_names: [...state.candidates_names.slice(0, action.payload[0]), action.payload[1], ...state.candidates_names.slice(action.payload[0] + 1)]
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
                sbs: false,
                n_voters: 1000,
                n_vacancies: 1,
                candidates: [],
                candidates_names: [],
                tactical_votes: [],
                minority_votes: []
            }    
        case SET_TACTICAL_PERC:
            return{
                ...state,
                tactical_votes: [...state.tactical_votes.slice(0, action.payload[0]), action.payload[1], ...state.tactical_votes.slice(action.payload[0] + 1)]
            }
        case SET_MINORITY_PERC:
            return{
                ...state,
                minority_votes: [...state.minority_votes.slice(0, action.payload[0]), action.payload[1], ...state.minority_votes.slice(action.payload[0] + 1)]
            }       
        default:
            return state;
    }
}