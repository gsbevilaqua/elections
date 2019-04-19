import { SET_ONE_ROUND, SET_TWO_ROUNDS, SET_IRV, SET_SBS, SET_FSB, SET_MVC, SET_NUMBER_CANDIDATES, SET_NUMBER_VOTERS, SET_NUMBER_VACANCIES, ADD_CANDIDATE, DELETE_CANDIDATE, SET_NAME, SET_FAME, RESET, SET_TACTICAL_PERC, SET_MINORITY_PERC, ADD_COALITION, ADD_CANDIDATE_TO_COALITION, DELETE_COALITION, SET_CANDIDATE } from '../actions/types.js'

const initial_state = {
    one_round: false,
    two_rounds: false,
    irv: false,
    sbs: false,
    fsb: false,
    mvc: false,
    n_voters: 1000,
    n_vacancies: 1,
    candidates: [],
    candidates_names: [],
    tactical_votes: [],
    minority_votes: [],
    coalitions: [],
    available: [],
    og_available: [],
    added_candidates: []
}

export default function(state = initial_state, action) {
    switch(action.type) {
        case SET_ONE_ROUND:
        return {
            ...state,
            one_round: !state.one_round
        }
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
        case SET_FSB:
            return {
                ...state,
                fsb: !state.fsb
            }
        case SET_MVC:
            return {
                ...state,
                mvc: !state.mvc
            }                      
        case SET_NUMBER_CANDIDATES:
            return {
                ...state,
                candidates: action.payload.fames,
                candidates_names: action.payload.names,
                tactical_votes: action.payload.tacts,
                minority_votes: action.payload.minos,
                available: action.payload.ava,
                og_available: action.payload.ava
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
                minority_votes: [...state.minority_votes, action.payload.mino],
                available: [...state.available, action.payload.index],
                og_available: [...state.available, action.payload.index]
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
                one_round: false,
                two_rounds: false,
                irv: false,
                sbs: false,
                fsb: false,
                mvc: false,
                n_voters: 1000,
                n_vacancies: 1,
                candidates: [],
                candidates_names: [],
                tactical_votes: [],
                minority_votes: [],
                coalitions: [],
                available: [],
                og_available: [],
                added_candidates: []
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
        case ADD_COALITION:
            return{
                ...state,
                coalitions: [...state.coalitions, []]
            }
        case DELETE_COALITION:
            state.coalitions = [...state.coalitions.slice(0, action.payload), ...state.coalitions.slice(action.payload + 1)]
            state.added_candidates = []
            state.available = state.og_available
            state.coalitions.forEach(element => {
                element.forEach(cand => {
                    state.added_candidates.push(cand);
                });
            });
            return{
                ...state,
                available: [...state.available.filter((x) => !state.added_candidates.includes(x))]
            }
        case ADD_CANDIDATE_TO_COALITION:
            return{
                ...state,
                coalitions: [...state.coalitions.slice(0, action.payload[0]), action.payload[1], ...state.coalitions.slice(action.payload[0] + 1)]
            }                        
        case SET_CANDIDATE:
            state.coalitions = [...state.coalitions.slice(0, action.payload[0]), [...state.coalitions[action.payload[0]].slice(0, action.payload[1]), action.payload[2], ...state.coalitions[action.payload[0]].slice(action.payload[1] + 1)], ...state.coalitions.slice(action.payload[0] + 1)]
            state.added_candidates = []
            state.available = state.og_available
            state.coalitions.forEach(element => {
                element.forEach(cand => {
                    state.added_candidates.push(cand)
                });
            });
            return{
                ...state,
                available: [...state.available.filter((x) => !state.added_candidates.includes(x))]
            }            
        default:
            return state;
    }
}