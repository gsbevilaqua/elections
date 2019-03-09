import React, { Component } from 'react'
import c3 from 'c3';

export default class Trs extends Component {
  constructor(props){
    super(props);
  }

  componentDidMount(){
    if(this.props.didRun){
      //console.log(this.props.res[0]);
      this.chart = c3.generate({
        bindto: "#pie1",
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
        bindto: "#bar1",
        data: {
            columns: this.props.res[0],
            type: 'bar'
        },
        bar: {
            width: 100 // this makes bar width 100px
        },
        size: {
          width:800
        }
      });
      this.chart = c3.generate({
        bindto: "#pie2",
        data: {
          columns: this.props.res[2],
          type : 'pie'
        },
        size: {
          width:300, 
          height:300
        }
      });
      this.chart = c3.generate({
        bindto: "#bar2",
        data: {
            columns: this.props.res[2],
            type: 'bar'
        },
        bar: {
            width: 100 // this makes bar width 100px
        },
        size: {
          width: 800
        }
      });
    }
  }
  
  render() {
    if(this.props.didRun){
        return (
        <div>
            <h1 style={{color: "aliceblue", fontSize: "2.5rem", padding: "1rem", background: "black"}}> T R S </h1>
            <div>
              <div style={{display: "grid", gridTemplateColumns: "50% 50%"}}>
                <div>
                  <div id="pie1"></div>
                </div>
                <div>
                  <div id="bar1"></div>
                </div>
              </div>
              <div className="container">
                <h2>MEAN: {this.props.res[1]}</h2>
              </div>
              <div style={{display: "grid", gridTemplateColumns: "50% 50%"}}>
                <div>
                  <div id="pie2"></div>
                </div>
                <div>
                  <div id="bar2"></div>
                </div>
              </div>
              <div>
                <h2>MEAN: {this.props.res[1]}</h2>
              </div>
            </div>
        </div>
        )
    }
    return null;
  }
}