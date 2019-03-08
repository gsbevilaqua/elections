import React, { Component } from 'react'
import c3 from 'c3';

export default class Irv extends Component {
  constructor(props){
    super(props);
  }

  componentDidMount(){
    if(this.props.didRun){
      console.log(this.props.res);
      let i = 0;
      this.props.res[0].forEach(element => {
        this.chart = c3.generate({
          bindto: "#chart" + i,
          data: {
            columns: this.props.res[0][i],
            type : 'pie'
          },
          size: {
            width:300, 
            height:300
          }
        });
        i++;
      });
    }
  }
  
  render() {
    if(this.props.didRun){
        return (
        <div style={{backgroundColor: "#ffcc80"}}>
            <h1 style={{color: "aliceblue", fontSize: "2.5rem", padding: "1rem", background: "black"}}> I R V </h1>
            <div>
              <div style={{display: "grid", gridTemplateColumns: "50% 50%", padding: "3rem"}}>
                { this.props.res[0].map((candidate, index) => (<div id={"chart" + index} key={index}></div>)) }
              </div>
            </div>
        </div>
        )
    }
    return null;
  }
}
