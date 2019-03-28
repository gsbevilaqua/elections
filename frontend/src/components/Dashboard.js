import React, { Component } from 'react'
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { setTwoRounds, setIrv, setNCandidates, setNVoters, setNVacancies, addCandidate, deleteCandidate, setName, setFame, fullReset } from "../actions/elections.js";
import axios from 'axios';
import { Redirect } from 'react-router-dom'

import Candidate from './Candidate';

export class Dashboard extends Component {
    constructor(props) {
        super(props);
        this.colorscheme = {0:'#006C6C', 1:'#950822', 2:'#053a5e', 3:'#f0f8ff', 4:'#292929'}
        this.fontcolor = {0:'white', 1:'white', 2:'white', 3:'black', 4:'white'};
        this.state = {
            redirect: false,
            progress_bar: false,
            progress_bar_width: "0%",
            progress_bar_msg: ""
        }
    }

    static propTypes ={
        two_rounds: PropTypes.bool.isRequired,
        irv: PropTypes.bool.isRequired,
        n_voters: PropTypes.number.isRequired,
        n_vacancies: PropTypes.number.isRequired,
        candidates: PropTypes.array.isRequired,
        candidates_names: PropTypes.array.isRequired
    }

    componentDidMount() {
        this.props.fullReset();
    }

    onBlurNVoters = (e) => this.props.setNVoters(e.target.value);
    onBlurNCandidates = (e) => this.props.setNCandidates(e.target.value);
    onBlurNVacancies = (e) => this.props.setNVacancies(e.target.value);

    renderRedirect = () => {
        if (this.state.redirect) {
          return <Redirect to={{ pathname: "/results", state: { go: true, trs_run: this.props.two_rounds, trs: this.state.trs, irv_run: this.props.irv, irv: this.state.irv } }}/>
        }
    }

    handleSubmit = () => {
        const payload = {
            two_rounds: this.props.two_rounds,
            irv: this.props.irv,
            n_voters: this.props.n_voters,
            n_vacancies: this.props.n_vacancies,
            candidates: this.props.candidates,
            candidates_names: this.props.candidates_names
        };

        this.handleAjaxRequest(payload);
    };

    handleAjaxRequest = (payload) => {
        const csrfToken = Cookies.get('csrftoken');

        const create_candidates_payload = { n_voters: payload.n_voters, candidates: payload.candidates, n_vacancies: payload.n_vacancies }
        const get_results_payload = { two_rounds: payload.two_rounds, irv: payload.irv }

        this.setState({ progress_bar: true, progress_bar_msg: "Creating Candidates..." });

        axios({
            method: 'post',
            url: '/api/create_candidates',
            data: create_candidates_payload,
            xsrfHeaderName: "X-CSRFToken",
        })
        .then(response => {
            this.setState({ progress_bar_width: "30%", progress_bar_msg: "Creating Voters..." });
            axios({
                method: 'post',
                url: '/api/create_voters',
                data: {},
                xsrfHeaderName: "X-CSRFToken",
            })
            .then(response => {
                this.setState({ progress_bar_width: "60%", progress_bar_msg: "Sorting Ranks..." });
                axios({
                    method: 'post',
                    url: '/api/sort_ranks',
                    data: {},
                    xsrfHeaderName: "X-CSRFToken",
                })
                .then(response => {
                    this.setState({ progress_bar_width: "90%", progress_bar_msg: "Finishing..." });
                    axios({
                        method: 'post',
                        url: '/api/get_results',
                        data: get_results_payload,
                        xsrfHeaderName: "X-CSRFToken",
                    })
                    .then(response => {
                        this.setState({ progress_bar_width: "100%" });
                        this.setState({ redirect: true, go: true, trs: response.data.status1, irv: response.data.status2 })
                    })
                    .catch(error => {
                        console.error(error);
                    })
                })
                .catch(error => {
                    console.error(error);
                })
            })
            .catch(error => {
                console.error(error);
            })
        })
        .catch(error => {
            console.error(error);
        })
    };

    render() {
        return (
            <div className="container" style={{display: 'grid', backgroundColor: '#e8e8e8', padding: '4rem'}}>
                {this.renderRedirect()}
                <br></br>
                <div style={{textAlign:'center'}}>
                    <h1 style={{padding:'1rem', fontFamily: "Bungee, cursive", fontSize: "3rem"}}> ELECTION SYSTEM </h1>
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
                    <div style={{display: "grid", gridTemplateColumns:"30% 20%"}}>
                        <h1 style={{padding:'1rem', margin: "auto", fontFamily: "Bungee, cursive"}}> CANDIDATES </h1>
                        <input onBlur={this.onBlurNCandidates} className="form-control" style={{height: "50%", margin: "auto"}} placeholder="Enter a number" />
                    </div>
                    <div className="candidates" style={{margin: '0 auto'}}>
                        {this.props.candidates.map((candidate, index) => (
                            <Candidate key={index} index={index} fame={candidate} color={this.colorscheme[index%5]} fontcolor={this.fontcolor[index%5]} setName={this.props.setName.bind(this)} setFame={this.props.setFame.bind(this)} deleteCandidate={this.props.deleteCandidate.bind(this)}/>
                        ))}
                        <div style={{padding:'2rem', textAlign: 'center'}}>
                            <button onClick={this.props.addCandidate.bind(this, 0, "Candidate " + this.props.candidates.length)} type="button" className="btn btn-primary btn-sm"><i className="fas fa-plus fa-5x"></i></button>
                            <h6 style={{padding: '1rem'}}> Add a candidate </h6>
                        </div>
                    </div>
                </div>
                <br></br>
                <div className="form-group">
                    <label style={{color: 'black', fontSize: '1rem'}}> N° of elected candidates: </label>
                    <input onBlur={this.onBlurNVacancies} className="form-control" placeholder="Enter a number" />
                    <small className="form-text text-muted"></small>
                </div>
                <br></br>
                <div>
                    <button onClick={this.handleSubmit.bind(this)} type="button" className="btn btn-info btn-lg" style={{width:'100%', fontFamily: "Germania One, cursive", fontSize: "2rem"}}>  Run </button>
                </div>
                {this.state.progress_bar ?
                    <div>
                        <div className="progress">
                            <div className="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100" style={{width: this.state.progress_bar_width}}></div>
                        </div>
                        <h3>{this.state.progress_bar_msg}</h3>
                    </div>
                    : ''
                }
            </div>
        );
    }
}

const mapStateToProps = state => ({
    two_rounds: state.electionsReducer.two_rounds,
    irv: state.electionsReducer.irv,
    n_voters: state.electionsReducer.n_voters,
    n_vacancies: state.electionsReducer.n_vacancies,
    candidates: state.electionsReducer.candidates,
    candidates_names: state.electionsReducer.candidates_names
});

export default connect(mapStateToProps, {setTwoRounds, setIrv, setNCandidates, setNVoters, setNVacancies, addCandidate, deleteCandidate, setName, setFame, fullReset})(Dashboard);