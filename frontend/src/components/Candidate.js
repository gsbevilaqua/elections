import React, { Component } from 'react';

export class Candidate extends Component {

    onBlurSetName = (e) => this.props.setName(this.props.index, e.target.value);
    onBlurSetTact = (e) => this.props.setTactical(this.props.index, e.target.value);
    onBlurSetMino = (e) => this.props.setMinority(this.props.index, e.target.value);

    render() {
        return (
            <div className="card text-white bg-primary mb-3">
                <div className="card-header" style={{display: "grid", gridTemplateColumns:"50% 25% 25%", backgroundColor:this.props.color, color:this.props.fontcolor}}>
                    <input onChange={this.onBlurSetName} className="form-control" style={{backgroundColor:this.props.color, color:this.props.fontcolor, fontSize: "1.2rem"}} value={this.props.name} placeholder={"Candidate " + this.props.index} />
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
                <div className="card-body" style={{backgroundColor:this.props.color, display: 'grid', gridTemplateColumns: '20% 70% 10%'}}>
                    <div style={{margin: '0 auto'}}>
                        <i className="far fa-user fa-5x"></i>
                    </div>
                    <div className="btn-group btn-group-toggle" data-toggle="buttons">
                        <label className={"btn btn-secondary btn-sm" + (this.props.fame == 4 ? ' active' : '')} >
                            <input onBlur={this.props.setFame.bind(this, this.props.index, 4)} type="radio" name="fame" id="loved" autoComplete="off"/> Loved
                        </label>
                        <label className={"btn btn-secondary btn-sm" + (this.props.fame == 3 ? ' active' : '')}>
                            <input onBlur={this.props.setFame.bind(this, this.props.index, 3)} type="radio" name="fame" id="liked" autoComplete="off"/> Liked
                        </label>
                        <label className={"btn btn-secondary btn-sm" + (this.props.fame == 0 ? ' active' : '')}>
                            <input onBlur={this.props.setFame.bind(this, this.props.index, 0)} type="radio" name="fame" id="neutral" autoComplete="off"/> Neutral
                        </label>
                        <label className={"btn btn-secondary btn-sm" + (this.props.fame == 2 ? ' active' : '')}>
                            <input onBlur={this.props.setFame.bind(this, this.props.index, 2)} type="radio" name="fame" id="disliked" autoComplete="off"/> Disliked
                        </label>
                        <label className={"btn btn-secondary btn-sm" + (this.props.fame == 1 ? ' active' : '')}>
                            <input onBlur={this.props.setFame.bind(this, this.props.index, 1)} type="radio" name="fame" id="hated" autoComplete="off"/> Hated
                        </label>
                        <label className={"btn btn-danger btn-sm" + (this.props.fame == -1 ? ' active' : '')}>
                            <input onBlur={this.props.setFame.bind(this, this.props.index, -1)} type="radio" name="fame" id="polarizer" autoComplete="off"/> Polarizer
                        </label>
                        <label className={"btn btn-secondary btn-sm" + (this.props.fame == -2 ? ' active' : '')} style={{backgroundColor:"#9a3734"}}>
                            <input onBlur={this.props.setFame.bind(this, this.props.index, -2)} type="radio" name="fame" id="most-polarizer" autoComplete="off"/> Most Polarizer
                        </label>
                    </div>
                    <div style={{margin: '0 auto', display:"flex", alignItems:"center"}}>
                        <button onClick={this.props.deleteCandidate.bind(this, this.props.index)} className="btn btn-primary btn-sm"><i className="fas fa-trash-alt fa-2x"></i></button>
                    </div>
                </div>
            </div>
        )
    }
}

export default Candidate;