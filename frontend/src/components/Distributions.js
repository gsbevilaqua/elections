import React, { Component } from 'react'
import { Link } from "react-router-dom";
import Chart from 'react-apexcharts'

export default class Details extends Component {
    constructor(props){
        super(props);
        this.state = {
            labels: { 
                neutral: "Neutral",
                liked: "Liked",
                disliked: "Disliked",
                loved: "Loved",
                hated: "Hated",
                polarizer: "Polarizer",
                more_polarizer: "More Polarizer"
            },
            ratings: [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            dists: {
                neutral: [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.03, 0.03, 0.73, 0.03, 0.03, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
                liked: [0.02, 0.03, 0.03, 0.03, 0.03, 0.04, 0.04, 0.04, 0.04, 0.04, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.06, 0.07, 0.08, 0.1],
                disliked: [0.1, 0.08, 0.07, 0.06, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.04, 0.04, 0.04, 0.04, 0.04, 0.03, 0.03, 0.03, 0.03, 0.02],
                loved: [0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.05, 0.05, 0.05, 0.05, 0.05, 0.075, 0.075, 0.1, 0.1, 0.125],
                hated: [0.125, 0.1, 0.1, 0.075, 0.075, 0.05, 0.05, 0.05, 0.05, 0.05, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025],
                polarizer: [0.1, 0.09, 0.09, 0.07, 0.06, 0.016, 0.016, 0.016, 0.016, 0.016, 0.02, 0.016, 0.016, 0.016, 0.016, 0.016, 0.06, 0.07, 0.09, 0.09, 0.1],
                more_polarizer: [0.15, 0.1, 0.1, 0.05, 0.05, 0.01, 0.01, 0.01, 0.01, 0.01, 0.0, 0.01, 0.01, 0.01, 0.01, 0.01, 0.05, 0.05, 0.1, 0.1, 0.15]
            },
            acum: {
                neutral: [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.11, 0.14, 0.87, 0.9, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1.0],
                liked: [0.02, 0.05, 0.08, 0.11, 0.14, 0.18, 0.22, 0.26, 0.3, 0.34, 0.39, 0.44, 0.49, 0.54, 0.59, 0.64, 0.69, 0.75, 0.82, 0.9, 1.0],
                disliked: [0.1, 0.18, 0.25, 0.31, 0.36, 0.41, 0.46, 0.51, 0.56, 0.61, 0.66, 0.7, 0.74, 0.78, 0.82, 0.86, 0.89, 0.92, 0.95, 0.98, 1.0],
                loved: [0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2, 0.225, 0.25, 0.275, 0.325, 0.375, 0.425, 0.475, 0.525, 0.6, 0.675, 0.775, 0.875, 1.0],
                hated: [0.125, 0.225, 0.325, 0.4, 0.475, 0.525, 0.575, 0.625, 0.675, 0.725, 0.75, 0.775, 0.8, 0.825, 0.85, 0.875, 0.9, 0.925, 0.95, 0.975, 1.0],
                polarizer: [0.1, 0.19, 0.28, 0.35, 0.41, 0.426, 0.442, 0.458, 0.474, 0.49, 0.51, 0.526, 0.542, 0.558, 0.574, 0.59, 0.65, 0.72, 0.81, 0.9, 1.0],
                more_polarizer: [0.15, 0.25, 0.35, 0.4, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.5, 0.51, 0.52, 0.53, 0.54, 0.55, 0.6, 0.65, 0.75, 0.85, 1.0]
            }
        }
    }

    render() {
        return (
            <div style={{textAlign: "center"}}>
                <h1 style={{fontSize: "5rem", padding: "2rem", background: "#826dc3", margin: "0", letterSpacing: "2rem"}}>DISTRIBUTIONS</h1>
                <div>
                    <h1 style={{color: "aliceblue", fontSize: "2.5rem", fontFamily: "Bungee, cursive", padding: "2rem", margin: "0", background: "black"}}> {this.state.labels.neutral} </h1>
                    <div style={{display: "grid", gridTemplateColumns: "50% 50%"}}>
                        <div style={{margin: "auto", paddingTop: "6rem", paddingLeft: "6rem", paddingRight: "4rem", paddingBottom: "3rem", backgroundColor: "#2B2D3E"}}>
                            <Chart options={{ chart: { id: "basic-bar" }, xaxis: { categories: this.state.ratings, labels:{style:{colors: '#ffffff', fontSize: '14px'}}}, yaxis:{labels:{style:{color: '#ffffff', fontSize: '14px'}}}, theme: {palette: 'palette6'}, title: {text: "PDF", style: { color: 'white' } }}}
                                    series={[{ name: "neutral", data: this.state.dists.neutral }]}
                                    type="bar"
                                    width="500"
                            />
                        </div>
                        <div style={{margin: "auto", paddingTop: "6rem", paddingLeft: "6rem", paddingRight: "4rem", paddingBottom: "3rem", backgroundColor: "#2B2D3E"}}>
                            <Chart options={{ chart: { id: "basic-bar" }, xaxis: { categories: this.state.ratings, labels:{style:{colors: '#ffffff', fontSize: '14px'}}}, yaxis:{labels:{style:{color: '#ffffff', fontSize: '14px'}}}, theme: {palette: 'palette6'}, title: {text: "CDF", style: { color: 'white' } }}}
                                    series={[{ name: "neutral_acum", data: this.state.acum.neutral }]}
                                    type="bar"
                                    width="500"
                            />
                        </div>
                    </div>
                </div>
                <div>
                    <h1 style={{color: "aliceblue", fontSize: "2.5rem", fontFamily: "Bungee, cursive", padding: "2rem", margin: "0", background: "black"}}> {this.state.labels.liked} </h1>
                    <div style={{display: "grid", gridTemplateColumns: "50% 50%"}}>
                        <div style={{margin: "auto", paddingTop: "6rem", paddingLeft: "6rem", paddingRight: "4rem", paddingBottom: "3rem", backgroundColor: "#2B2D3E"}}>
                            <Chart options={{ chart: { id: "basic-bar" }, xaxis: { categories: this.state.ratings, labels:{style:{colors: '#ffffff', fontSize: '14px'}}}, yaxis:{labels:{style:{color: '#ffffff', fontSize: '14px'}}}, theme: {palette: 'palette6'}, title: {text: "PDF", style: { color: 'white' } }}}
                                    series={[{ name: "liked", data: this.state.dists.liked }]}
                                    type="bar"
                                    width="500"
                            />
                        </div>
                        <div style={{margin: "auto", paddingTop: "6rem", paddingLeft: "6rem", paddingRight: "4rem", paddingBottom: "3rem", backgroundColor: "#2B2D3E"}}>
                            <Chart options={{ chart: { id: "basic-bar" }, xaxis: { categories: this.state.ratings, labels:{style:{colors: '#ffffff', fontSize: '14px'}}}, yaxis:{labels:{style:{color: '#ffffff', fontSize: '14px'}}}, theme: {palette: 'palette6'}, title: {text: "CDF", style: { color: 'white' } }}}
                                    series={[{ name: "liked_acum", data: this.state.acum.liked }]}
                                    type="bar"
                                    width="500"
                            />
                        </div>
                    </div>
                </div>
                <div>
                    <h1 style={{color: "aliceblue", fontSize: "2.5rem", fontFamily: "Bungee, cursive", padding: "2rem", margin: "0", background: "black"}}> {this.state.labels.disliked} </h1>
                    <div style={{display: "grid", gridTemplateColumns: "50% 50%"}}>
                        <div style={{margin: "auto", paddingTop: "6rem", paddingLeft: "6rem", paddingRight: "4rem", paddingBottom: "3rem", backgroundColor: "#2B2D3E"}}>
                            <Chart options={{ chart: { id: "basic-bar" }, xaxis: { categories: this.state.ratings, labels:{style:{colors: '#ffffff', fontSize: '14px'}}}, yaxis:{labels:{style:{color: '#ffffff', fontSize: '14px'}}}, theme: {palette: 'palette6'}, title: {text: "PDF", style: { color: 'white' } }}}
                                    series={[{ name: "disliked", data: this.state.dists.disliked }]}
                                    type="bar"
                                    width="500"
                            />
                        </div>
                        <div style={{margin: "auto", paddingTop: "6rem", paddingLeft: "6rem", paddingRight: "4rem", paddingBottom: "3rem", backgroundColor: "#2B2D3E"}}>
                            <Chart options={{ chart: { id: "basic-bar" }, xaxis: { categories: this.state.ratings, labels:{style:{colors: '#ffffff', fontSize: '14px'}}}, yaxis:{labels:{style:{color: '#ffffff', fontSize: '14px'}}}, theme: {palette: 'palette6'}, title: {text: "CDF", style: { color: 'white' } }}}
                                    series={[{ name: "disliked_acum", data: this.state.acum.disliked }]}
                                    type="bar"
                                    width="500"
                            />
                        </div>
                    </div>
                </div>
                <div>
                    <h1 style={{color: "aliceblue", fontSize: "2.5rem", fontFamily: "Bungee, cursive", padding: "2rem", margin: "0", background: "black"}}> {this.state.labels.loved} </h1>
                    <div style={{display: "grid", gridTemplateColumns: "50% 50%"}}>
                        <div style={{margin: "auto", paddingTop: "6rem", paddingLeft: "6rem", paddingRight: "4rem", paddingBottom: "3rem", backgroundColor: "#2B2D3E"}}>
                            <Chart options={{ chart: { id: "basic-bar" }, xaxis: { categories: this.state.ratings, labels:{style:{colors: '#ffffff', fontSize: '14px'}}}, yaxis:{labels:{style:{color: '#ffffff', fontSize: '14px'}}}, theme: {palette: 'palette6'}, title: {text: "PDF", style: { color: 'white' } }}}
                                    series={[{ name: "loved", data: this.state.dists.loved }]}
                                    type="bar"
                                    width="500"
                            />
                        </div>
                        <div style={{margin: "auto", paddingTop: "6rem", paddingLeft: "6rem", paddingRight: "4rem", paddingBottom: "3rem", backgroundColor: "#2B2D3E"}}>
                            <Chart options={{ chart: { id: "basic-bar" }, xaxis: { categories: this.state.ratings, labels:{style:{colors: '#ffffff', fontSize: '14px'}}}, yaxis:{labels:{style:{color: '#ffffff', fontSize: '14px'}}}, theme: {palette: 'palette6'}, title: {text: "CDF", style: { color: 'white' } }}}
                                    series={[{ name: "loved_acum", data: this.state.acum.loved }]}
                                    type="bar"
                                    width="500"
                            />
                        </div>
                    </div>
                </div>
                <div>
                    <h1 style={{color: "aliceblue", fontSize: "2.5rem", fontFamily: "Bungee, cursive", padding: "2rem", margin: "0", background: "black"}}> {this.state.labels.hated} </h1>
                    <div style={{display: "grid", gridTemplateColumns: "50% 50%"}}>
                        <div style={{margin: "auto", paddingTop: "6rem", paddingLeft: "6rem", paddingRight: "4rem", paddingBottom: "3rem", backgroundColor: "#2B2D3E"}}>
                            <Chart options={{ chart: { id: "basic-bar" }, xaxis: { categories: this.state.ratings, labels:{style:{colors: '#ffffff', fontSize: '14px'}}}, yaxis:{labels:{style:{color: '#ffffff', fontSize: '14px'}}}, theme: {palette: 'palette6'}, title: {text: "PDF", style: { color: 'white' } }}}
                                    series={[{ name: "hated", data: this.state.dists.hated }]}
                                    type="bar"
                                    width="500"
                            />
                        </div>
                        <div style={{margin: "auto", paddingTop: "6rem", paddingLeft: "6rem", paddingRight: "4rem", paddingBottom: "3rem", backgroundColor: "#2B2D3E"}}>
                            <Chart options={{ chart: { id: "basic-bar" }, xaxis: { categories: this.state.ratings, labels:{style:{colors: '#ffffff', fontSize: '14px'}}}, yaxis:{labels:{style:{color: '#ffffff', fontSize: '14px'}}}, theme: {palette: 'palette6'}, title: {text: "CDF", style: { color: 'white' } }}}
                                    series={[{ name: "hated_acum", data: this.state.acum.hated }]}
                                    type="bar"
                                    width="500"
                            />
                        </div>
                    </div>
                </div>
                <div>
                    <h1 style={{color: "aliceblue", fontSize: "2.5rem", fontFamily: "Bungee, cursive", padding: "2rem", margin: "0", background: "black"}}> {this.state.labels.polarizer} </h1>
                    <div style={{display: "grid", gridTemplateColumns: "50% 50%"}}>
                        <div style={{margin: "auto", paddingTop: "6rem", paddingLeft: "6rem", paddingRight: "4rem", paddingBottom: "3rem", backgroundColor: "#2B2D3E"}}>
                            <Chart options={{ chart: { id: "basic-bar" }, xaxis: { categories: this.state.ratings, labels:{style:{colors: '#ffffff', fontSize: '14px'}}}, yaxis:{labels:{style:{color: '#ffffff', fontSize: '14px'}}}, theme: {palette: 'palette6'}, title: {text: "PDF", style: { color: 'white' } }}}
                                    series={[{ name: "polarizer", data: this.state.dists.polarizer }]}
                                    type="bar"
                                    width="500"
                            />
                        </div>
                        <div style={{margin: "auto", paddingTop: "6rem", paddingLeft: "6rem", paddingRight: "4rem", paddingBottom: "3rem", backgroundColor: "#2B2D3E"}}>
                            <Chart options={{ chart: { id: "basic-bar" }, xaxis: { categories: this.state.ratings, labels:{style:{colors: '#ffffff', fontSize: '14px'}}}, yaxis:{labels:{style:{color: '#ffffff', fontSize: '14px'}}}, theme: {palette: 'palette6'}, title: {text: "CDF", style: { color: 'white' } }}}
                                    series={[{ name: "polarizer_acum", data: this.state.acum.polarizer }]}
                                    type="bar"
                                    width="500"
                            />
                        </div>
                    </div>
                </div>
                <div>
                <h1 style={{color: "aliceblue", fontSize: "2.5rem", fontFamily: "Bungee, cursive", padding: "2rem", margin: "0", background: "black"}}> {this.state.labels.more_polarizer} </h1>
                    <div style={{display: "grid", gridTemplateColumns: "50% 50%"}}>
                        <div style={{margin: "auto", paddingTop: "6rem", paddingLeft: "6rem", paddingRight: "4rem", paddingBottom: "3rem", backgroundColor: "#2B2D3E"}}>
                            <Chart options={{ chart: { id: "basic-bar" }, xaxis: { categories: this.state.ratings, labels:{style:{colors: '#ffffff', fontSize: '14px'}}}, yaxis:{labels:{style:{color: '#ffffff', fontSize: '14px'}}}, theme: {palette: 'palette6'}, title: {text: "PDF", style: { color: 'white' } }}}
                                    series={[{ name: "more_polarizer", data: this.state.dists.more_polarizer }]}
                                    type="bar"
                                    width="500"
                            />
                        </div>
                        <div style={{margin: "auto", paddingTop: "6rem", paddingLeft: "6rem", paddingRight: "4rem", paddingBottom: "3rem", backgroundColor: "#2B2D3E"}}>
                            <Chart options={{ chart: { id: "basic-bar" }, xaxis: { categories: this.state.ratings, labels:{style:{colors: '#ffffff', fontSize: '14px'}}}, yaxis:{labels:{style:{color: '#ffffff', fontSize: '14px'}}}, theme: {palette: 'palette6'}, title: {text: "CDF", style: { color: 'white' } }}}
                                    series={[{ name: "more_polarizer_acum", data: this.state.acum.more_polarizer }]}
                                    type="bar"
                                    width="500"
                            />
                        </div>
                    </div>
                </div>
                <Link to="/">
                    <button type="button" className="btn btn-info btn-lg" style={{width:'100%', fontFamily: "Germania One, cursive", fontSize: "2rem"}}>  Back </button>
                </Link>
            </div>
        )
    }
}
