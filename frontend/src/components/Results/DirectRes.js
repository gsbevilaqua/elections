import React, { Component } from 'react'
import axios from 'axios';
import { Redirect } from 'react-router-dom'

export default class DirectRes extends Component {
    constructor(props) {
        super(props);
        this.state = { go: null }
    }

    componentDidMount() {
        this.handleSubmit();
    }

    handleSubmit = () => {
        var systems = [false, false, false, false, false, false, false];

        var i = this.props.match.params.systems.length;
        while (i--) {
            if(this.props.match.params.systems.charAt(i) == 1){
                systems[i] = true;
            }
        }
        this.setState({ors_run: systems[0], trs_run: systems[1], irv_run: systems[2], avs_run: systems[3], tbc_run: systems[4], svs_run: systems[5], bvs_run: systems[6]})

        var voters = []
        if(this.props.match.params.voters !== '-'){
            var str = this.props.match.params.voters.split(',')
            
            i = str.length
            var j = i/3
            
            for (j = 0; j < i/3; j++) {
                str[j*3 + 2] = str[j*3 + 2].split(' ')
                for (var k = 0; k < str[j*3 + 2].length; k++){
                str[j*3 + 2][k] = parseInt(str[j*3 + 2][k])
                }
                let voter = {pop_percentage: str[j*3], name: str[j*3 + 1], scores: str[j*3 + 2]}
                voters.push(voter)
            }
        }

        const payload = {
            one_round: systems[0],
            two_rounds: systems[1],
            irv: systems[2],
            avs: systems[3],
            tbc: systems[4],
            svs: systems[5],
            bvs: systems[6],
            n_voters: this.props.match.params.n_voters === '-' ? 1000 : this.props.match.params.n_voters,
            n_vacancies: this.props.match.params.n_vacancies === '-' ? 1 : this.props.match.params.n_vacancies,
            candidates:  this.props.match.params.candidates === '-' ? [0, 0, 0] : JSON.parse(this.props.match.params.candidates),
            candidates_names:  this.props.match.params.names === '-' ? ["Candidate 0", "Candidate 1", "Candidate 2"] : JSON.parse(this.props.match.params.names),
            tactical: this.props.match.params.tc === '-' ? false : true,
            minority: this.props.match.params.mc === '-' ? false : true,
            tactical_votes: this.props.match.params.tv === '-' ? [0, 0, 0] : JSON.parse(this.props.match.params.tv),
            minority_votes: this.props.match.params.mv === '-' ? [0, 0, 0] : JSON.parse(this.props.match.params.mv),
            coalitions: this.props.match.params.coal === '-' ? [] : JSON.parse(this.props.match.params.coal),
            voters: this.props.match.params.voters === '-' ? [] : voters,
            seed: this.props.match.params.seed === '-' ? null : this.props.match.params.seed
        };

        this.handleAjaxRequest(payload);
    };
    
    handleAjaxRequest = (payload) => {

        axios({
            method: 'post',
            url: '/api/direct_results',
            data: payload,
            xsrfHeaderName: "X-CSRFToken",
        })
        .then(response => {
            this.setState({ go: true, ors: response.data.status, trs: response.data.status1, irv: response.data.status2, avs: response.data.status6, tbc: response.data.status4, svs: response.data.status3, bvs: response.data.status5 })
        })
        .catch(error => {
            console.error(error);
        })
    };    

    render() {
        const { go } = this.state;

        if (go === null) {
            return null;
        }

        return <Redirect to={{ pathname: "/results", state: { go: true, ors_run: this.state.ors_run, ors: this.state.ors, trs_run: this.state.trs_run, trs: this.state.trs, irv_run: this.state.irv_run, irv: this.state.irv, avs_run: this.state.avs_run, avs: this.state.avs, tbc_run: this.state.tbc_run, tbc: this.state.tbc, svs_run: this.state.svs_run, svs: this.state.svs, bvs_run: this.state.bvs_run, bvs: this.state.bvs } }}/>
    }
}
