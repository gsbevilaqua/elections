import { combineReducers } from 'redux';
import elections from './electionsReducer';

export default combineReducers({
    electionsReducer: elections
});