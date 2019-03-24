import React, { Component } from 'react';

export class Candidate extends Component {
  render() {
    return (
        <div className="card text-white bg-primary mb-3">
            <div className="card-header" style={{backgroundColor:this.props.color, color:this.props.fontcolor}}>Candidate {this.props.index}</div>
            <div className="card-body" style={{backgroundColor:this.props.color, display: 'grid', gridTemplateColumns: '20% 70% 10%'}}>
                <div style={{margin: '0 auto'}}>
                    <i className="far fa-user fa-5x"></i>
                </div>
                <div className="btn-group btn-group-toggle" data-toggle="buttons">
                    <label className="btn btn-secondary btn-sm">
                        <input onBlur={this.props.setFame.bind(this, this.props.index, 4)} type="radio" name="fame" id="loved" autoComplete="off"/> Loved
                    </label>
                    <label className="btn btn-secondary btn-sm">
                        <input onBlur={this.props.setFame.bind(this, this.props.index, 3)} type="radio" name="fame" id="liked" autoComplete="off"/> Liked
                    </label>
                    <label className="btn btn-secondary btn-sm active">
                        <input onBlur={this.props.setFame.bind(this, this.props.index, 0)} type="radio" name="fame" id="neutral" autoComplete="off"/> Neutral
                    </label>
                    <label className="btn btn-secondary btn-sm">
                        <input onBlur={this.props.setFame.bind(this, this.props.index, 2)} type="radio" name="fame" id="disliked" autoComplete="off"/> Disliked
                    </label>
                    <label className="btn btn-secondary btn-sm">
                        <input onBlur={this.props.setFame.bind(this, this.props.index, 1)} type="radio" name="fame" id="hated" autoComplete="off"/> Hated
                    </label>
                    <label className="btn btn-danger btn-sm">
                        <input onBlur={this.props.setFame.bind(this, this.props.index, -1)} type="radio" name="fame" id="polarizer" autoComplete="off"/> Polarizer
                    </label>
                    <label className="btn btn-danger btn-sm" style={{backgroundColor:"#9a3734"}}>
                        <input onBlur={this.props.setFame.bind(this, this.props.index, -2)} type="radio" name="fame" id="most-polarizer" autoComplete="off"/> Most Polarizer
                    </label>
                </div>
                <div style={{margin: '0 auto'}}>
                    <button onClick={this.props.deleteCandidate.bind(this, this.props.index)} className="btn btn-primary btn-sm"><i className="fas fa-trash-alt fa-2x"></i></button>
                </div>
            </div>
        </div>
    )
  }
}

export default Candidate;