import React, { Component } from 'react'
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { Link } from "react-router-dom";
import { setTwoRounds, setIrv, setNVoters, addCandidate, deleteCandidate, setFame, fullReset } from "../actions/elections.js";

import Candidate from './Candidate';

export class Dashboard extends Component {
    constructor(props) {
        super(props);
        this.colorscheme = {0:'#006C6C', 1:'#b70324c7', 2:'#00416cd1', 3:'#f0f8ff', 5:'#292929'}
        this.fontcolor = {0:'white', 1:'white', 2:'white', 3:'black', 5:'white'};
    }

    static propTypes ={
        two_rounds: PropTypes.bool.isRequired,
        irv: PropTypes.bool.isRequired,
        n_voters: PropTypes.number.isRequired,
        candidates: PropTypes.array.isRequired,
    }

    componentDidMount() {
        this.props.fullReset();
    }

    onBlurNVoters = (e) => this.props.setNVoters(e.target.value);

    render() {
        return (
            <div className="container" style={{display: 'grid'}}>
                <br></br>
                <div style={{textAlign:'center'}}>
                    <h1 style={{padding:'1rem'}}> ELECTION SYSTEM </h1>
                    <br></br>
                    <div style={{textAlign:'center'}} className="btn-group btn-group-toggle" data-toggle="buttons">
                        <button style={{margin:'1rem'}} onClick={this.props.setTwoRounds.bind(this)} type="checkbox" className="btn btn-outline-primary btn-lg" data-toggle="tooltip" data-placement="left" title="" data-original-title="The two-round system is a voting method used to elect a single winner, where the voter casts a single vote for their chosen candidate.">2 Round System</button>
                        <button style={{margin:'1rem'}} onClick={this.props.setIrv.bind(this)} type="checkbox" className="btn btn-outline-primary btn-lg" data-toggle="tooltip" data-placement="right" title="" data-original-title="Instead of voting only for a single candidate, voters in IRV elections can rank the candidates in order of preference.">Instant-runoff Voting</button>
                    </div>
                </div>
                <br></br><br></br>
                <div className="form-group">
                    <label style={{color: 'black', fontSize: '1rem'}}> N° of voters: </label>
                    <input onBlur={this.onBlurNVoters} className="form-control" placeholder="Enter a number" />
                    <small className="form-text text-muted"></small>
                </div>
                <br></br><br></br><br></br>
                <div>
                    <h1 style={{padding:'1rem'}}> CANDIDATES </h1>
                    <div className="candidates" style={{margin: '0 auto'}}>
                        {this.props.candidates.map((candidate, index) => (
                            <Candidate key={index} index={index} color={this.colorscheme[index%5]} fontcolor={this.fontcolor[index%5]} setFame={this.props.setFame.bind(this)} deleteCandidate={this.props.deleteCandidate.bind(this)}/>
                        ))}
                        <div style={{padding:'2rem', textAlign: 'center'}}>
                            <button onClick={this.props.addCandidate.bind(this, 0)} type="button" className="btn btn-primary btn-sm"><i className="fas fa-plus fa-5x"></i></button>
                            <h6 style={{padding: '1rem'}}> Add a candidate </h6>
                        </div>
                    </div>
                </div>
                <br></br>
                <div>
                    <Link to={{ pathname: "/results", state: {two_rounds:this.props.two_rounds, irv:this.props.irv,
                                                      n_voters:this.props.n_voters, candidates:this.props.candidates}
                              }}>
                        <button type="button" className="btn btn-info btn-lg" style={{width:'100%'}}>  Run </button>
                    </Link>
                </div>
            </div>
        );
    }
}

const mapStateToProps = state => ({
    two_rounds: state.electionsReducer.two_rounds,
    irv: state.electionsReducer.irv,
    n_voters: state.electionsReducer.n_voters,
    candidates: state.electionsReducer.candidates
});

export default connect(mapStateToProps, {setTwoRounds, setIrv, setNVoters, addCandidate, deleteCandidate, setFame, fullReset})(Dashboard);