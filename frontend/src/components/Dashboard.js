import React, { Component } from 'react'
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { setOneRound, setTwoRounds, setIrv, setAvs, setTbc, setSvs, setBvs, 
         setNCandidates, setNVoters, setNVacancies, addCandidate, deleteCandidate, setName, 
         setFame, fullReset, setTactical, setMinority, addCoalition, addCandidateToCoalition, 
         deleteCoalition, setCandidate, setNProfiles, addVoter, deleteVoter, setCandidateScore, 
         setProfileName, setProfilePerc, setSeed, errorSys, errorCan, errorVac, manipulateMode, generateMode } from "../actions/elections.js";
import axios from 'axios';
import { Redirect } from 'react-router-dom'

import Candidate from './Candidate';
import CandidateMan from './CandidateMan';
import Voter from './Voter';
import Coalition from './Coalition';

export class Dashboard extends Component {
    constructor(props) {
        super(props);
        this.colorscheme = {0:'#006C6C', 1:'#950822', 2:'#053a5e', 3:'#f0f8ff', 4:'#292929'}
        this.fontcolor = {0:'white', 1:'white', 2:'white', 3:'black', 4:'white'};
        this.state = {
            redirect: false,
            progress_bar: false,
            progress_bar_width: "0%",
            progress_bar_msg: "",
            tactical_checked: false,
            minority_checked: false,
            error_msg: "",
            disable_trs: "",
            disable_irv: "",
            disable_bv: "disabled"
        }
    }

    static propTypes ={
        one_round: PropTypes.bool.isRequired,
        two_rounds: PropTypes.bool.isRequired,
        irv: PropTypes.bool.isRequired,
        avs: PropTypes.bool.isRequired,
        tbc: PropTypes.bool.isRequired,
        svs: PropTypes.bool.isRequired,
        bvs: PropTypes.bool.isRequired,
        n_voters: PropTypes.number.isRequired,
        n_vacancies: PropTypes.number.isRequired,
        candidates: PropTypes.array.isRequired,
        candidates_names: PropTypes.array.isRequired,
        tactical_votes: PropTypes.array.isRequired,
        minority_votes: PropTypes.array.isRequired,
        coalitions: PropTypes.array.isRequired,
        available_candidates: PropTypes.array.isRequired,
        voters: PropTypes.array.isRequired,
        errors: PropTypes.array.isRequired
    }

    componentDidMount() {
        this.props.fullReset();
    }

    setTrs = () => { if (!(this.state.disable_trs.length > 0)) this.props.setTwoRounds() }
    setIrv = () => { if (!(this.state.disable_irv.length > 0)) this.props.setIrv() }
    setBvs = () => { if (!(this.state.disable_bv.length > 0)) this.props.setBvs() }
    
    onBlurNVoters = (e) => this.props.setNVoters(e.target.value);
    onBlurNCandidates = (e) => this.props.setNCandidates(e.target.value);
    onBlurNVacancies = (e) => {
        if (e.target.value > 1) {
            this.state.disable_trs = "disabled";
            this.state.disable_irv = "disabled";
            this.state.disable_bv = "";
            if (this.props.trs == true){
                this.props.setTwoRounds();
            }
            if (this.props.irv == true){
                this.props.setIrv();
            }
        } else {
            this.state.disable_trs = "";
            this.state.disable_irv = "";
            this.state.disable_bv = "disabled";
            if (this.props.bvs == true){
                this.props.setBvs();
            }
        }
        this.props.setNVacancies(e.target.value);
    }
    onBlurNProfiles = (e) => this.props.setNProfiles(e.target.value);
    onBlurSeed = (e) => this.props.setSeed(e.target.value);

    toggleTacticalCheckbox = (e) => this.setState({[e.target.name]:e.target.checked});
    toggleMinorityCheckbox = (e) => this.setState({[e.target.name]:e.target.checked});

    setCandidate = (coalition_index, candidate_index, candidate_name) => {
        this.props.setCandidate(coalition_index, candidate_index, candidate_name);
    }

    tabManipulate = () => {
        this.setState({tactical_checked: false, minority_checked: false});
        this.props.manipulateMode();
    }

    tabGenerate = () => {
        this.setState({tactical_checked: false, minority_checked: false});
        this.props.generateMode();
    }

    renderRedirect = () => {
        if (this.state.redirect) {
          return <Redirect to={{ pathname: "/results", state: { go: true, ors_run: this.props.one_round, ors: this.state.ors, trs_run: this.props.two_rounds, trs: this.state.trs, irv_run: this.props.irv, irv: this.state.irv, avs_run: this.props.avs, avs: this.state.avs, tbc_run: this.props.tbc, tbc: this.state.tbc, svs_run: this.props.svs, svs: this.state.svs, bvs_run: this.props.bvs, bvs: this.state.bvs } }}/>
        }
    }

    handleErrors = () => {
        if (this.props.one_round == false & this.props.two_rounds == false & this.props.irv == false
            & this.props.avs == false & this.props.tbc == false & this.props.svs == false & this.props.bvs == false){
                this.props.errorSys();
                this.setState({
                    error_msg: "Please select a voting system"
                });
        }

        if (this.props.candidates.length < 3){
            this.props.errorCan();
            this.setState({
                error_msg: "Number of candidates must be at least 3"
            });
        }        

        if (this.props.candidates.length - this.props.n_vacancies <= 0){
            this.props.errorVac();
            this.setState({
                error_msg: "Number of candidates must be at least one more than number of vacancies"
            });
        }
    }

    handleSubmit = () => {
        this.handleErrors();

        if (this.props.errors.length == 0){
            this.setState({
                error_msg: ""
            });
            const payload = {
                one_round: this.props.one_round,
                two_rounds: this.props.two_rounds,
                irv: this.props.irv,
                avs: this.props.avs,
                tbc: this.props.tbc,
                svs: this.props.svs,
                bvs: this.props.bvs,
                n_voters: this.props.n_voters,
                n_vacancies: this.props.n_vacancies,
                candidates: this.props.candidates,
                candidates_names: this.props.candidates_names,
                tactical: this.state.tactical_checked,
                minority: this.state.minority_checked,
                tactical_votes: this.props.tactical_votes,
                minority_votes: this.props.minority_votes,
                coalitions: this.props.coalitions,
                voters: this.props.voters,
                seed: this.props.seed
            };

            this.handleAjaxRequest(payload);
        }
    };

    handleAjaxRequest = (payload) => {
        const csrfToken = Cookies.get('csrftoken');

        const create_candidates_payload = { n_voters: payload.n_voters, candidates: payload.candidates, candidates_names: payload.candidates_names, tactical: payload.tactical, minority: payload.minority, tactical_votes: payload.tactical_votes, minority_votes: payload.minority_votes, coalitions: payload.coalitions, n_vacancies: payload.n_vacancies, voters: payload.voters, seed: payload.seed }
        const get_results_payload = { one_round: payload.one_round, two_rounds: payload.two_rounds, irv: payload.irv, avs: payload.avs, tbc: payload.tbc, svs: payload.svs, bvs: payload.bvs }

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
                        this.setState({ redirect: true, go: true, ors: response.data.status, trs: response.data.status1, irv: response.data.status2, avs: response.data.status6, tbc: response.data.status4, svs: response.data.status3, bvs: response.data.status5 })
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
            <div className="container" style={{display: 'grid', backgroundColor: '#fff', padding: '4rem'}}>
                {this.renderRedirect()}
                <br></br>
                <div style={{textAlign:'center'}}>
                    <h1 style={{padding:'1rem', fontSize: "3rem"}}> ELECTION SYSTEM </h1>
                    <br></br>
                    <div style={{display:'block'}} className="btn-group btn-group-toggle" data-toggle="buttons">
                        <div>
                            <button style={{margin:'1rem'}} onClick={this.props.setOneRound.bind(this)} type="checkbox" className="btn btn-outline-primary btn-lg" data-toggle="tooltip" data-placement="left" title="" data-original-title="The first past the post system is a voting method used to elect a single winner, where the voter casts a single vote for their chosen candidate.">First Past The Post</button>
                            <button style={{margin:'1rem'}} onClick={this.setTrs} type="checkbox" className={"btn btn-outline-primary btn-lg " + this.state.disable_trs} data-toggle="tooltip" data-placement="top" title="" data-original-title="The two-round system is a voting method used to elect a single winner, where the voter casts a single vote for their chosen candidate. The 2 best placed candidates go to a second round.">2 Round System</button>
                            <button style={{margin:'1rem'}} onClick={this.setIrv} type="checkbox" className={"btn btn-outline-primary btn-lg " + this.state.disable_irv} data-toggle="tooltip" data-placement="right" title="" data-original-title="Instead of voting only for a single candidate, voters in IRV can rank the candidates in order of preference and each round the worst ranked candidate is eliminated.">Instant-runoff Voting</button>
                        </div>
                        <div>
                            <button style={{margin:'1rem'}} onClick={this.props.setAvs.bind(this)} type="checkbox" className="btn btn-outline-primary btn-lg" data-toggle="tooltip" data-placement="left" title="" data-original-title="In this system voters rank the candidates by preference, each rank has a fixed score, the candidate(s) with the highest sum of scores wins.">Appoval Voting System</button>
                            <button style={{margin:'1rem'}} onClick={this.props.setTbc.bind(this)} type="checkbox" className="btn btn-outline-primary btn-lg" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="In this system voters rank the candidates by preference, each rank has a fixed score, the candidate(s) with the highest sum of scores wins.">The Borda Count</button>
                            <button style={{margin:'1rem'}} onClick={this.props.setSvs.bind(this)} type="checkbox" className="btn btn-outline-primary btn-lg" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="In this system voters give scores to every candidate, the candidate(s) with the highest sum of scores wins.">Score Voting System</button>
                            <button style={{margin:'1rem'}} onClick={this.setBvs} type="checkbox" className={"btn btn-outline-primary btn-lg " + this.state.disable_bv} data-toggle="tooltip" data-placement="right" title="" data-original-title="In this system voters can vote for as many candidates as the number of candidates elected">Bloc Vote</button>
                        </div>
                    </div>
                </div>
                <br></br><br></br>
                <div className="form-group">
                    <label style={{color: 'black', fontSize: '1rem'}}> Seed of Simulation: </label>
                    <input onBlur={this.onBlurSeed} className="form-control" placeholder="Enter a number" />
                    <small className="form-text text-muted"></small>
                </div>
                <br></br><br></br>
                <div className="form-group">
                    <label style={{color: 'black', fontSize: '1rem'}}> N° of voters: </label>
                    <input onBlur={this.onBlurNVoters} className="form-control" placeholder="Enter a number" />
                    <small className="form-text text-muted"></small>
                </div>
                <br></br><br></br>
                <div className="form-group">
                    <label style={{color: 'black', fontSize: '1rem'}}> N° of elected candidates: </label>
                    <input onBlur={this.onBlurNVacancies} className="form-control" placeholder="Enter a number" />
                    <small className="form-text text-muted"></small>
                </div>                
                <br></br><br></br>
                <div className="line-break" style={{height:"0.15rem", width:"100%", backgroundColor:"rgba(128, 128, 128, 0.40)"}}></div>
                <br></br><br></br>
                <ul className="nav nav-tabs">
                    <li className="nav-item">
                        <a onClick={this.tabManipulate} className="nav-link active" data-toggle="tab" href="#manipulate">Manipulate</a>
                    </li>
                    <li className="nav-item">
                        <a onClick={this.tabGenerate} className="nav-link" data-toggle="tab" href="#generate">Generate</a>
                    </li>
                </ul>
                <div id="myTabContent" className="tab-content">
                    <br></br><br></br>
                    <div className="tab-pane fade active show" id="manipulate">
                        <div>
                            <div style={{display: "grid", gridTemplateColumns:"30% 20% 25% 25%"}}>
                                <h1 style={{padding:'1rem'}}> CANDIDATES </h1>
                                <input onBlur={this.onBlurNCandidates} className="form-control" style={{height: "50%", margin: "auto"}} placeholder="Enter a number" />
                                <div style={{margin: "auto"}} className="custom-control custom-checkbox">
                                    <input type="checkbox" className="custom-control-input" id="tactical-check" name="tactical_checked" checked={this.state.tactical_checked} onChange={this.toggleTacticalCheckbox} />
                                    <label className="custom-control-label" htmlFor="tactical-check">Tactical Voting</label>
                                </div>
                                <div style={{margin: "auto"}} className="custom-control custom-checkbox">
                                    <input type="checkbox" className="custom-control-input" id="minority-check" name="minority_checked" checked={this.state.minority_checked} onChange={this.toggleMinorityCheckbox} />
                                    <label className="custom-control-label" htmlFor="minority-check">Minority Voting</label>
                                </div>
                            </div>

                            <div className="candidates" style={{margin: '0 auto'}}>
                                {this.props.candidates.map((candidate, index) => (
                                    <CandidateMan key={index} index={index} fame={candidate} name={this.props.candidates_names[index]} tactical={this.state.tactical_checked} minority={this.state.minority_checked} color={this.colorscheme[index%5]} fontcolor={this.fontcolor[index%5]} setName={this.props.setName.bind(this)} setFame={this.props.setFame.bind(this)} deleteCandidate={this.props.deleteCandidate.bind(this)} setTactical={this.props.setTactical.bind(this)} setMinority={this.props.setMinority.bind(this)}/>
                                ))}
                                <div style={{padding:'2rem', textAlign: 'center'}}>
                                    <button onClick={this.props.addCandidate.bind(this, 0, "Candidate " + this.props.candidates.length, 0.0, 0.0, this.props.candidates.length)} type="button" className="btn btn-primary btn-sm"><i className="fas fa-plus fa-5x"></i></button>
                                    <h6 style={{padding: '1rem'}}> Add a candidate </h6>
                                </div>
                            </div>
                        </div>
                        <br></br><br></br>
                        <div className="line-break" style={{height:"0.15rem", width:"100%", backgroundColor:"rgba(128, 128, 128, 0.40)"}}></div>
                        <br></br><br></br>                        
                        <div>
                            <div style={{display: "grid", gridTemplateColumns:"40% 20%"}}>
                                <h1 style={{padding:'1rem'}}> VOTERS PROFILES </h1>
                                <input onBlur={this.onBlurNProfiles} className="form-control" style={{height: "50%", margin: "auto"}} placeholder="Enter a number" />
                            </div>

                            <div className="voters" style={{margin: '0 auto'}}>
                                {this.props.voters.map((voter, index) => (
                                    <Voter key={index} index={index} pop_percentage={voter.pop_percentage} name={voter.name} candidates={this.props.candidates_names} scores={voter.scores} color={this.colorscheme[index%5]} fontcolor={this.fontcolor[index%5]} deleteVoter={this.props.deleteVoter} setCandidateScore={this.props.setCandidateScore}  setProfileName={this.props.setProfileName.bind(this)} setProfilePerc={this.props.setProfilePerc} />
                                ))}
                                <div style={{padding:'2rem', textAlign: 'center'}}>
                                    <button onClick={this.props.addVoter.bind(this, 0, "Voter Profile " + this.props.voters.length, 0.0)} type="button" className="btn btn-primary btn-sm"><i className="fas fa-plus fa-5x"></i></button>
                                    <h6 style={{padding: '1rem'}}> Add a profile </h6>
                                </div>
                            </div>
                        </div>
                        <br></br><br></br>
                        <div>
                            <div>
                                <h1 style={{padding:'1rem', margin: "auto"}}> COALITIONS </h1>
                            </div>
                            <div className="coalitions" style={{margin: '0 auto'}}>
                                {this.props.coalitions.map((coalition, index) => (
                                    <Coalition key={index} index={index} candidates={this.props.coalitions[index]} available_candidates={this.props.available_candidates} color={this.colorscheme[index%5]} fontcolor={this.fontcolor[index%5]} addCandidateToCoalition={this.props.addCandidateToCoalition.bind(this)} setCandidate={this.setCandidate} deleteCoalition={this.props.deleteCoalition.bind(this)}/>
                                ))}
                                <div style={{padding:'2rem', textAlign: 'center'}}>
                                    <button onClick={this.props.addCoalition.bind(this)} type="button" className="btn btn-primary btn-sm"><i className="fas fa-plus fa-5x"></i></button>
                                    <h6 style={{padding: '1rem'}}> Add a coalition </h6>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="tab-pane fade" id="generate">
                        <div>
                            <div style={{display: "grid", gridTemplateColumns:"30% 20% 25% 25%"}}>
                                <h1 style={{padding:'1rem'}}> CANDIDATES </h1>
                                <input onBlur={this.onBlurNCandidates} className="form-control" style={{height: "50%", margin: "auto"}} placeholder="Enter a number" />
                                <div style={{margin: "auto"}} className="custom-control custom-checkbox">
                                    <input type="checkbox" className="custom-control-input" id="tactical-check" name="tactical_checked" checked={this.state.tactical_checked} onChange={this.toggleTacticalCheckbox} />
                                    <label className="custom-control-label" htmlFor="tactical-check">Tactical Voting</label>
                                </div>
                                <div style={{margin: "auto"}} className="custom-control custom-checkbox">
                                    <input type="checkbox" className="custom-control-input" id="minority-check" name="minority_checked" checked={this.state.minority_checked} onChange={this.toggleMinorityCheckbox} />
                                    <label className="custom-control-label" htmlFor="minority-check">Minority Voting</label>
                                </div>
                            </div>

                            <div className="candidates" style={{margin: '0 auto'}}>
                                {this.props.candidates.map((candidate, index) => (
                                    <Candidate key={index} index={index} fame={candidate} name={this.props.candidates_names[index]} tactical={this.state.tactical_checked} minority={this.state.minority_checked} color={this.colorscheme[index%5]} fontcolor={this.fontcolor[index%5]} setName={this.props.setName.bind(this)} setFame={this.props.setFame.bind(this)} deleteCandidate={this.props.deleteCandidate.bind(this)} setTactical={this.props.setTactical.bind(this)} setMinority={this.props.setMinority.bind(this)}/>
                                ))}
                                <div style={{padding:'2rem', textAlign: 'center'}}>
                                    <button onClick={this.props.addCandidate.bind(this, 0, "Candidate " + this.props.candidates.length, 0.0, 0.0, this.props.candidates.length)} type="button" className="btn btn-primary btn-sm"><i className="fas fa-plus fa-5x"></i></button>
                                    <h6 style={{padding: '1rem'}}> Add a candidate </h6>
                                </div>
                            </div>
                        </div>
                        <br></br><br></br>
                        <div className="line-break" style={{height:"0.15rem", width:"100%", backgroundColor:"rgba(128, 128, 128, 0.40)"}}></div>
                        <br></br><br></br>
                        <div>
                            <div>
                                <h1 style={{padding:'1rem', margin: "auto"}}> COALITIONS </h1>
                            </div>
                            <div className="coalitions" style={{margin: '0 auto'}}>
                                {this.props.coalitions.map((coalition, index) => (
                                    <Coalition key={index} index={index} candidates={this.props.coalitions[index]} available_candidates={this.props.available_candidates} color={this.colorscheme[index%5]} fontcolor={this.fontcolor[index%5]} addCandidateToCoalition={this.props.addCandidateToCoalition.bind(this)} setCandidate={this.setCandidate} deleteCoalition={this.props.deleteCoalition.bind(this)}/>
                                ))}
                                <div style={{padding:'2rem', textAlign: 'center'}}>
                                    <button onClick={this.props.addCoalition.bind(this)} type="button" className="btn btn-primary btn-sm"><i className="fas fa-plus fa-5x"></i></button>
                                    <h6 style={{padding: '1rem'}}> Add a coalition </h6>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>             
                <br></br>
                <div>
                    <button onClick={this.handleSubmit.bind(this)} type="button" className="btn btn-info btn-lg" style={{width:'100%', fontFamily: "Germania One, cursive", fontSize: "2rem", borderRadius: "0.5rem"}}>  Run </button>
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
                <br></br><br></br>
                {this.state.error_msg != "" ?
                    <div className="card text-white" style={{backgroundColor: "#d9534fc2", borderRadius: "0.5rem"}}>
                        <div className="card-body">
                            <h4 className="card-title">ERROR:</h4>
                            <p className="card-text">{this.state.error_msg}</p>
                        </div>
                    </div>
                    : ""
                }
            </div>
        );
    }
}

const mapStateToProps = state => ({
    one_round: state.electionsReducer.one_round,    
    two_rounds: state.electionsReducer.two_rounds,
    irv: state.electionsReducer.irv,
    avs: state.electionsReducer.avs,
    tbc: state.electionsReducer.tbc,
    svs: state.electionsReducer.svs,
    bvs: state.electionsReducer.bvs,
    n_voters: state.electionsReducer.n_voters,
    n_vacancies: state.electionsReducer.n_vacancies,
    candidates: state.electionsReducer.candidates,
    candidates_names: state.electionsReducer.candidates_names,
    tactical_votes: state.electionsReducer.tactical_votes,
    minority_votes: state.electionsReducer.minority_votes,
    coalitions: state.electionsReducer.coalitions,
    available_candidates: state.electionsReducer.available,
    voters: state.electionsReducer.voters,
    seed: state.electionsReducer.seed,
    errors: state.electionsReducer.errors
});

export default connect(mapStateToProps, { setOneRound, setTwoRounds, setIrv, setAvs, setTbc, setSvs, setBvs, 
                        setNCandidates, setNVoters, setNVacancies, addCandidate, deleteCandidate, setName, 
                        setFame, fullReset, setTactical, setMinority, addCoalition, addCandidateToCoalition, 
                        deleteCoalition, setCandidate, setNProfiles, addVoter, deleteVoter, setCandidateScore, 
                        setProfileName, setProfilePerc, setSeed, errorSys, errorCan, errorVac, manipulateMode, generateMode })(Dashboard);
