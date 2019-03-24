import React, { Component } from 'react'
import Chart from 'react-apexcharts'

export default class Irv extends Component {
  constructor(props){
    super(props);
    this.state = {
      options: {
        plotOptions: {
          radialBar: {
            startAngle: -135,
            endAngle: 135,
            dataLabels: {
              name: {
                fontSize: '16px',
                color: undefined,
                offsetY: 120
              },
              value: {
                offsetY: 76,
                fontSize: '22px',
                color: undefined,
                formatter: function (val) {
                  return val + "%";
                }
              }
            }
          }
        },
        fill: {
          type: 'gradient',
          gradient: {
            shade: 'dark',
            shadeIntensity: 0.15,
            inverseColors: false,
            opacityFrom: 1,
            opacityTo: 1,
            stops: [0, 50, 65, 91]
          },
        },
        stroke: {
          dashArray: 4
        },
        labels: ['Satisfaction Rate']
      },
      series: [67],
    }
  }

  componentDidMount(){
    console.log(this.props.res);
  }

  render() {
    if(this.props.didRun){
      return (
        <div style={{backgroundColor: "#343e59"}}>
            <h1 style={{color: "aliceblue", fontSize: "2.5rem", padding: "1rem", background: "black"}}> I R V </h1>
            <div style={{padding:"4rem"}}>
              { this.props.res[0].map((_, index) => 
                (<div key={index} style={{display: "grid", gridTemplateColumns: "50% 50%", padding: "3rem"}}>
                  <div style={{margin: "auto", paddingTop: "5rem", paddingLeft: "6rem", paddingRight: "4rem", backgroundColor: "#2B2D3E"}}>
                    <Chart options={{labels: this.props.res[0][index][0], theme: {palette: 'palette4'}, legend:{fontSize: '14px', labels:{colors: '#ffffff'}}}}
                      series={this.props.res[0][index][1]}
                      type="pie"
                      width="380"
                    />
                  </div>
                  <div style={{margin: "auto", paddingTop: "6rem", paddingLeft: "6rem", paddingRight: "4rem", paddingBottom: "3rem", backgroundColor: "#2B2D3E"}}>
                    <Chart options={{xaxis:{categories: this.props.res[0][index][0], labels:{style:{colors: '#ffffff', fontSize: '14px'}}}, yaxis:{labels:{style:{color: '#ffffff', fontSize: '14px'}}}, theme:{palette: 'palette8'}}}
                          series={[{name: "series-1", data: this.props.res[0][index][1] }]}
                          type="bar"
                          width="500"
                    />
                  </div>
                </div>)) }
                <div style={{backgroundColor: "#FFFFFF", margin: "auto", padding: "3rem", paddingRight: "6rem", paddingLeft: "6rem"}}>
                  <Chart options={this.state.options} 
                        series={[(((this.props.res[1] + 10)/2)*10).toFixed(2)]} 
                        type="radialBar" 
                        height="350"
                  />
                </div>
            </div>
        </div>
      )
    }
    return null;
  }
}
