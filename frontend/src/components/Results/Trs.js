import React, { Component } from 'react'
import c3 from 'c3';

export default class Trs extends Component {
  constructor(props){
    super(props);
  }

  componentDidMount(){
    if(this.props.didRun){
      console.log(this.props.res[0]);
      this.chart = c3.generate({
        bindto: "#chart",
        data: {
          columns: this.props.res[0],
          type : 'pie'
        },
        size: {
          width:300, 
          height:300
        }
      });
      this.chart = c3.generate({
        bindto: "#chart2",
        data: {
          columns: this.props.res[2],
          type : 'pie'
        },
        size: {
          width:300, 
          height:300
        }
      });
    }
  }
  
  render() {
    if(this.props.didRun){
        return (
        <div style={{backgroundColor: "#989898"}}>
            <h1 style={{color: "aliceblue", fontSize: "2.5rem", padding: "1rem", background: "black"}}> T R S </h1>
            <div style={{display: "grid", gridTemplateColumns: "50% 50%"}}>
              <div>
                <div id="chart"></div>
                <h2>MEAN: {this.props.res[1]}</h2>
              </div>
              <div>
                <div id="chart2"></div>
                <h2>MEAN: {this.props.res[1]}</h2>
              </div>
            </div>
        </div>
        )
    }
    return null;
  }
}