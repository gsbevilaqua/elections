import React, { Component } from 'react';

export class CandidateMan extends Component {

    onBlurSetName = (e) => this.props.setName(this.props.index, e.target.value);
    onBlurSetTact = (e) => this.props.setTactical(this.props.index, e.target.value);
    onBlurSetMino = (e) => this.props.setMinority(this.props.index, e.target.value);

    render() {
        return (
            <div className="card text-white bg-primary mb-3">
                <div className="card-header" style={{backgroundColor:this.props.color, color:this.props.fontcolor}}>
                    <input onChange={this.onBlurSetName} className="form-control" style={{backgroundColor:this.props.color, color:this.props.fontcolor, fontSize: "1.2rem"}} value={this.props.name} placeholder={"Candidate " + this.props.index} />
                </div>
                <div className="card-body" style={{backgroundColor:this.props.color, display: 'grid', gridTemplateColumns: '20% 70% 10%'}}>
                    <div style={{margin: '0 auto'}}>
                        <i className="far fa-user fa-5x"></i>
                    </div>
                    <div style={{display: "grid", gridTemplateColumns:"50% 50%",}}>
                        {this.props.tactical ?
                            <div className="form-group">
                                <label style={{marginLeft:"25%"}} htmlFor="tacticalVote">Tactical Votes Percentage</label>
                                <select onChange={this.onBlurSetTact} style={{width:"50%", marginLeft:"25%"}} className="form-control" id="tacticalVote">
                                    <option val="0.0">0.0</option>
                                    <option val="0.1">0.1</option>
                                    <option val="0.2">0.2</option>
                                    <option val="0.3">0.3</option>
                                    <option val="0.4">0.4</option>
                                    <option val="0.5">0.5</option>
                                    <option val="0.6">0.6</option>
                                    <option val="0.7">0.7</option>
                                    <option val="0.8">0.8</option>
                                    <option val="0.9">0.9</option>
                                    <option val="1.0">1.0</option>
                                </select>
                            </div>
                            : ''
                        }
                        {this.props.minority ?
                            <div className="form-group">
                                <label style={{marginLeft:"25%"}} htmlFor="minorityVote">Minority Votes Percentage</label>
                                <select onChange={this.onBlurSetMino} style={{width:"50%", marginLeft:"25%"}} className="form-control" id="minorityVote">
                                    <option val="0.0">0.0</option>
                                    <option val="0.1">0.1</option>
                                    <option val="0.2">0.2</option>
                                    <option val="0.3">0.3</option>
                                    <option val="0.4">0.4</option>
                                    <option val="0.5">0.5</option>
                                    <option val="0.6">0.6</option>
                                    <option val="0.7">0.7</option>
                                    <option val="0.8">0.8</option>
                                    <option val="0.9">0.9</option>
                                    <option val="1.0">1.0</option>
                                </select>
                            </div>
                            : ''
                        }                        
                    </div>
                    <div style={{margin: '0 auto', display:"flex", alignItems:"center"}}>
                        <button onClick={this.props.deleteCandidate.bind(this, this.props.index)} className="btn btn-primary btn-sm"><i className="fas fa-trash-alt fa-2x"></i></button>
                    </div>
                </div>
            </div>
        )
    }
}

export default CandidateMan;