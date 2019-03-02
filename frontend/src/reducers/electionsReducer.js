import { SET_TWO_ROUNDS, SET_IRV, SET_NUMBER_VOTERS, ADD_CANDIDATE, DELETE_CANDIDATE, SET_FAME } from '../actions/types.js'

const initial_state = {
    two_rounds: false,
    irv: false,
    n_voters: 1000,
    candidates: []
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
        case SET_NUMBER_VOTERS:
            return{
                ...state,
                n_voters: action.payload
            }
        case ADD_CANDIDATE:
            return{
                ...state,
                candidates: [...state.candidates, action.payload]
            }
        case DELETE_CANDIDATE:
            return{
                ...state,
                candidates: [...state.candidates.slice(0, action.payload), ...state.candidates.slice(action.payload + 1)]
            }

        case SET_FAME:
            return{
                ...state,
                candidates: [...state.candidates.slice(0, action.payload[0]), action.payload[1], ...state.candidates.slice(action.payload[0] + 1)]
            }                        
        default:
            return state;
    }
}