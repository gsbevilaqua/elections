import React, { Component } from 'react'
import axios from 'axios';

import Trs from './Trs.js';
import Irv from './Irv.js';

export default class Results extends Component {
    constructor(props) {
        super(props);
        this.state = { go: null, trs: null, irv: null };
    }

    componentDidMount() {
        this.handleSubmit();
    }

    handleSubmit = () => {
        // Gathering together the data to send to API
        const payload = {
            two_rounds: this.props.location.state.two_rounds,
            irv: this.props.location.state.irv,
            n_voters: this.props.location.state.n_voters,
            candidates: this.props.location.state.candidates
        };

        // Method we're using to send data to API
        this.handleAjaxRequest(payload);
    };

    // Method to send data to backend
    handleAjaxRequest = (payload) => {
        const csrfToken = Cookies.get('csrftoken');

        axios({
            method: 'post',
            url: '/api/get_results',
            data: payload,
            xsrfHeaderName: "X-CSRFToken",
        })
        .then(response => {
            this.setState({ go: true, trs: response.data.status1, irv: response.data.status2 })
            //console.log(this.state);
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

        return (
            <div>
                <h1>RESULTS</h1>
                <Trs didRun={this.props.location.state.two_rounds} res={this.state.trs} />
                <Irv didRun={this.props.location.state.irv} res={this.state.irv} />
            </div>
        )
    }
}
