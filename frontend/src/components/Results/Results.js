import React, { Component } from 'react'
import { Link } from "react-router-dom";

import Fptp from './Fptp.js';
import Trs from './Trs.js';
import Irv from './Irv.js';
import Sbs from './Sbs.js';
import Fsb from './Fsb.js';
import Mvc from './Mvc.js';

export default class Results extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        const { go } = this.props.location.state;

        if (go === null) {
          return null;
        }

        return (
            <div style={{textAlign: "center"}}>
                <h1 style={{fontSize: "5rem", padding: "2rem", background: "#826dc3", margin: "0", letterSpacing: "2rem"}}>RESULTS</h1>
                <Fptp didRun={this.props.location.state.ors_run} res={this.props.location.state.ors} />
                <Trs didRun={this.props.location.state.trs_run} res={this.props.location.state.trs} />
                <Sbs didRun={this.props.location.state.sbs_run} res={this.props.location.state.sbs} />
                <Fsb didRun={this.props.location.state.fsb_run} res={this.props.location.state.fsb} />
                <Irv didRun={this.props.location.state.irv_run} res={this.props.location.state.irv} />
                <Mvc didRun={this.props.location.state.mvc_run} res={this.props.location.state.mvc} />
                <Link to="/">
                    <button type="button" className="btn btn-info btn-lg" style={{width:'100%', fontFamily: "Germania One, cursive", fontSize: "2rem"}}>  Back </button>
                </Link>
            </div>
        )
    }
}
