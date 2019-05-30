import React, { Component } from 'react'
import Chart from 'react-apexcharts'

export default class Svs extends Component {
  constructor(props){
    super(props);
    let mean = this.props.res[1]
    this.state = {
      points: this.props.didRun ? this.props.res[2].map((e) => ({ 
        x: e,
        seriesIndex: 0,
        label: {
          borderColor: '#775DD0',
          offsetY: 0,
          style: {
            color: '#fff',
            background: '#775DD0',
          },
          text: 'Elected!',
        }
      })) : [],
      options1: {
        colors: ["#992f41"],
        plotOptions: {
          radialBar: {
            startAngle: -90,
            endAngle: 90,
            track: {
              background: '#333',
              startAngle: -90,
              endAngle: 90,
            },
            dataLabels: {
              name: {
                offsetY: -10,
                color: "#fff",
                fontSize: "13px"
              },
              value: {
                fontSize: "30px",
                color: "#fff",
                show: true,
                formatter: function (val) {
                  if(mean > 0){
                    return '+' + mean.toFixed(3)
                  }
                  else{
                    return mean.toFixed(3)
                  }
                }
              }
            }
          }
        },
        fill: {
          type: "gradient",
          gradient: {
            shade: "dark",
            type: "horizontal",
            gradientToColors: ["#1fa83a"],
            stops: [0, 100]
          }
        },
        stroke: {
          lineCap: "butt"
        },
        labels: ["Mean"]
      },    
      options2: {
        plotOptions: {
          radialBar: {
            startAngle: -135,
            endAngle: 225,
            hollow: {
              margin: 0,
              size: '70%',
              background: "#293450",
              image: undefined,
              imageOffsetX: 0,
              imageOffsetY: 0,
              position: 'front',
              dropShadow: {
                enabled: true,
                top: 3,
                left: 0,
                blur: 4,
                opacity: 0.24
              }
            },
            track: {
              background: '#fff',
              strokeWidth: '67%',
              margin: 0, // margin is in pixels
              dropShadow: {
                enabled: true,
                top: -3,
                left: 0,
                blur: 4,
                opacity: 0.35
              }
            },
  
            dataLabels: {
              showOn: 'always',
              name: {
                offsetY: -10,
                show: true,
                color: "#fff",
                fontSize: '17px'
              },
              value: {
                color: "#fff",
                fontSize: '36px',
                show: true
              }
            }
          }
        },
        fill: {
          type: 'gradient',
          gradient: {
            shade: 'dark',
            type: 'horizontal',
            shadeIntensity: 0.5,
            gradientToColors: ['#ABE5A1'],
            inverseColors: true,
            opacityFrom: 1,
            opacityTo: 1,
            stops: [0, 100]
          }
        },
        series: [75],
        stroke: {
          lineCap: 'round'
        },
        labels: ['Satisfaction Rate'],      
      }
    }
  }

  render() {
    if(this.props.didRun){
      return (
        <div style={{backgroundColor: "#2b2d3e"}}>
            <h1 style={{color: "aliceblue", fontSize: "2.5rem", fontFamily: "Bungee, cursive", padding: "2rem", background: "black"}}> APPROVAL VOTING SYSTEM </h1>
            <div style={{padding:"4rem"}}>            
                <div style={{display:"flex", justifyContent:"center"}}>
                  <div style={{display: "grid", gridTemplateColumns: "50% 50%"}}>
                    <div style={{margin: "auto", backgroundColor: "#2B2D3E"}}>
                    <Chart options={{annotations: {points: this.state.points}, dataLabels: {enabled: true,dropShadow: {enabled: true,left: 2,top: 2,opacity: 0.5}}, colors: ["#46adfb"], xaxis:{categories: this.props.res[0][0], labels:{style:{colors: '#ffffff'}}}, yaxis:{title:{text:"Scores", style:{color:'white'}},labels:{style:{color: '#ffffff', fontSize: '14px'}}}, theme:{palette: 'palette8'}, fill: {type: 'gradient',gradient: {shade: 'light',type: "horizontal",shadeIntensity: 0.25,gradientToColors: undefined,inverseColors: true,opacityFrom: 0.85,opacityTo: 0.85,stops: [50, 0, 100]}}}}
                            series={[{name: "series-1", data: this.props.res[0][1] }]}
                            type="bar"
                            width="500"
                    />
                    </div> 
                    {/* <div style={{margin: "auto", paddingTop: "5rem", backgroundColor: "#2B2D3E"}}>
                      <Chart options={{labels: this.props.res[0][0], theme: {palette: 'palette4'}, legend:{fontSize: '14px', labels:{colors: '#ffffff'}}}}
                        series={this.props.res[0][1]}
                        type="pie"
                        width="380"
                      />
                    </div> */}
                  </div>
                </div>
                <div style={{display: "grid", gridTemplateColumns: "50% 50%"}}>
                  <div>
                    <Chart options={this.state.options1} 
                          series={[((this.props.res[1] + 10)*5).toFixed(2)]} 
                          type="radialBar"
                          height="350"
                    />
                  </div>
                  <div>
                    <Chart options={this.state.options2} 
                          series={[(this.props.res[3]*100).toFixed(2)]} 
                          type="radialBar"
                          height="350"
                    />
                  </div>
                </div>
            </div>
        </div>
      )
    }
    return null;
  }
}
