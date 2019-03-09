import React, { Component } from 'react'
import c3 from 'c3';

export default class Irv extends Component {
  constructor(props){
    super(props);
  }

  componentDidMount(){
    if(this.props.didRun){
      //console.log(this.props.res);
      let i = 0;
      this.props.res[0].forEach(element => {
        this.chart = c3.generate({
          bindto: "#pie" + i,
          data: {
            columns: this.props.res[0][i],
            type : 'pie'
          },
          size: {
            width:300, 
            height:300
          }
        });
        this.chart = c3.generate({
          bindto: "#bar" + i,
          data: {
              columns: this.props.res[0][i],
              type: 'bar'
          },
          bar: {
              width: 50, // this makes bar width 100px
              ratio: 0.8
          },
          size: {
            width:800
          }
        });
        i++;
      });
    }
  }
  
  render() {
    if(this.props.didRun){
        return (
        <div style={{backgroundColor: "#ffcc807a"}}>
            <h1 style={{color: "aliceblue", fontSize: "2.5rem", padding: "1rem", background: "black"}}> I R V </h1>
            <div>
              <div>
                { this.props.res[0].map((_, index) => 
                  (<div key={index} style={{display: "grid", gridTemplateColumns: "50% 50%", padding: "3rem"}}>
                    <div id={"pie" + index}></div>
                    <div id={"bar" + index}></div>
                  </div>)) }
              </div>
            </div>
        </div>
        )
    }
    return null;
  }
}
