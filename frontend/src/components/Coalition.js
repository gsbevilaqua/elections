import React, { Component } from 'react';
import Select from 'react-select';

export class Coalition extends Component {

    constructor(props){
        super(props);
        this.state = {
            selected: []
        }
    }

    handleOnChange(candidate_index, value) {
        this.setState({
            selected: [...this.state.selected.slice(0, candidate_index), value, ...this.state.selected.slice(candidate_index)]
        });
        this.props.setCandidate(this.props.index, candidate_index, value)
    }

    render() {
        return (
            <div className="card text-white bg-primary mb-3">
                <div className="card-header" style={{backgroundColor:this.props.color, color:this.props.fontcolor}}>
                    <h1 style={{backgroundColor:this.props.color, color:this.props.fontcolor, fontSize: "1.2rem"}}>{"Coalition " + this.props.index}</h1>
                </div>
                <div className="card-body" style={{backgroundColor:this.props.color, display: 'grid', gridTemplateColumns: '90% 10%'}}>
                    <div className="coalition-candidates" style={{display: "flex"}}>
                        {this.props.candidates.map((candidate_name, candidate_index) => (
                            <div key={candidate_index} style={{display:"flex", alignItems:"center", padding:"0.5rem"}}>
                                <div style={{display:"block", textAlign:"center"}}>
                                    <div style={{margin: '0 auto', padding:"0.5rem"}}>
                                        <i className="far fa-user fa-3x"></i>
                                    </div>
                                    <div style={{width:"10rem", color:"black"}}>
                                        <Select
                                            multi={false}
                                            options={this.props.available_candidates}
                                            onChange={this.handleOnChange.bind(this, candidate_index)}
                                            value={this.state.selected[candidate_index]}
                                            showNewOptionAtTop={false}
                                        />
                                    </div>
                                </div>
                            </div>
                        ))}
                        <div style={{padding:'1rem', textAlign: 'center'}}>
                            <button onClick={this.props.addCandidateToCoalition.bind(this, this.props.index, this.props.candidates)} type="button" className="btn btn-primary btn-sm"><i className="fas fa-plus fa-2x"></i></button>
                            <h6 style={{padding: '0.5rem', letterSpacing:"0.1rem", color:this.props.fontcolor}}> Add Candidate </h6>
                        </div>
                    </div>
                    <div style={{margin: '0 auto', display:"flex", alignItems:"center"}}>
                        <button onClick={this.props.deleteCoalition.bind(this, this.props.index)} className="btn btn-primary btn-sm"><i className="fas fa-trash-alt fa-2x"></i></button>
                    </div>
                </div>
            </div>
        )
    }
}

export default Coalition;