import React, { Component } from 'react';
import Select from 'react-select';

export class Voter extends Component {

    constructor(props){
        super(props);
        this.state = {
            options: [  {value: 10, label: "+10"},
                        {value: 9, label: "+9"},
                        {value: 8, label: "+8"},
                        {value: 7, label: "+7"},
                        {value: 6, label: "+6"},
                        {value: 5, label: "+5"},
                        {value: 4, label: "+4"},
                        {value: 3, label: "+3"},
                        {value: 2, label: "+2"},
                        {value: 1, label: "+1"},
                        {value: 0, label: "0"},
                        {value: -1, label: "-1"},
                        {value: -2, label: "-2"},
                        {value: -3, label: "-3"},
                        {value: -4, label: "-4"},
                        {value: -5, label: "-5"},
                        {value: -6, label: "-6"},
                        {value: -7, label: "-7"},
                        {value: -8, label: "-8"},
                        {value: -9, label: "-9"},
                        {value: -10, label: "-10"}  ],
            selected: [],
            name: this.props.name
        }
    }

    onBlurSetName = (e) => { 
        this.props.setProfileName(this.props.index, e.target.value)
        this.setState({
            name: e.target.value
        })
    }
    onBlurSetPerc = (e) => this.props.setProfilePerc(this.props.index, e.target.value)

    handleOnChange(candidate_index, value) {
        this.state.selected[candidate_index] = value
        this.props.setCandidateScore(value, this.props.index, candidate_index)
    }

    render() {
        return (
            <div className="card text-white bg-primary mb-3">
                <div className="card-header" style={{backgroundColor:this.props.color, color:this.props.fontcolor, display: "grid", gridTemplateColumns:"50% 50%"}}>
                <input onChange={this.onBlurSetName} className="form-control" style={{backgroundColor:this.props.color, color:this.props.fontcolor, fontSize: "1.2rem"}} value={this.state.name} placeholder={"Voter Profile " + this.props.index} />
                    <div className="form-group" style={{margin:"auto"}}>
                        <label className="control-label">Population percentage</label>
                        <div className="form-group">
                            <div className="input-group mb-3">
                                <input onChange={this.onBlurSetPerc} type="text" className="form-control" aria-label="Amount (to the nearest dollar)" placeholder="Enter a number" />
                                <div className="input-group-append">
                                    <span className="input-group-text">%</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="card-body" style={{backgroundColor:this.props.color, display: 'grid', gridTemplateColumns: '20% 70% 10%'}}>
                    <div style={{margin: '0 auto'}}>
                        <i className="far fa-user fa-5x"></i>
                    </div>
                    <div className="voter-candidates" style={{display: "flex", flexWrap: "wrap", justifyContent: "center", alignItems: "center"}}>
                        {this.props.candidates.length ? this.props.candidates.map((candidate_name, candidate_index) => (
                            <div key={candidate_index} style={{backgroundColor:"white", display:"flex", alignItems:"center", padding:"0.5rem", borderRadius: "0.5rem", margin: "0.3rem"}}>
                                <div style={{display:"block", textAlign:"center"}}>
                                    <div style={{margin: '0 auto'}}>
                                        <h6 style={{letterSpacing: "0"}}>{candidate_name}</h6>
                                    </div>
                                    <div style={{width:"5rem", color:"black"}}>
                                        <Select
                                            multi={false}
                                            options={this.state.options}
                                            onChange={this.handleOnChange.bind(this, candidate_index)}
                                            value={this.state.selected[candidate_index]}
                                            showNewOptionAtTop={false}
                                        />
                                    </div>
                                </div>
                            </div>
                        )) : 
                            <h1 style={{fontStyle: "oblique", fontWeight: "bold", color: "white"}}> NO CANDIDATES </h1>
                        }
                    </div>
                    <div style={{margin: '0 auto', display:"flex", alignItems:"center"}}>
                        <button onClick={this.props.deleteVoter.bind(this, this.props.index)} className="btn btn-primary btn-sm"><i className="fas fa-trash-alt fa-2x"></i></button>
                    </div>
                </div>
            </div>
        )
    }
}

export default Voter;