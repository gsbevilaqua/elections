import React, { Component } from 'react'
import ReactDOM from 'react-dom';
import Chart from 'react-apexcharts';
import c3 from 'c3';

export default class Irv extends Component {
  constructor(props){
    super(props);
  }

  componentDidMount(){
    console.log(this.props.res);
  }
  
  render() {
    if(this.props.didRun){
        return (
        <div>
            <h1> I R V </h1>
        </div>
        )
    }
    return null;
  }
}
