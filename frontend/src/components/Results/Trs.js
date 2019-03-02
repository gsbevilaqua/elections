import React, { Component } from 'react'
import ReactDOM from 'react-dom';
import Chart from 'react-apexcharts';
import c3 from 'c3';

export default class Trs extends Component {
  constructor(props){
    super(props);
  }

  componentDidMount(){
    this.chart = c3.generate({
      bindto: "#chart",
      data: {
        columns: this.props.res[0],
        type : 'pie'
      }
    });
    this.chart = c3.generate({
      bindto: "#chart2",
      data: {
        columns: this.props.res[2],
        type : 'pie'
      }
    });
  }
  
  render() {
    if(this.props.didRun){
        return (
        <div>
            <h1> T R S </h1>
            <div>
              <div id="chart"></div>
              <h2>MEAN: {this.props.res[1]}</h2>
              <div id="chart2"></div>
              <h2>MEAN: {this.props.res[1]}</h2>
            </div>
        </div>
        )
    }
    return null;
  }
}