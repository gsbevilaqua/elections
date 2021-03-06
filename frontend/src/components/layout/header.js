import React, { Component } from 'react'
import Link from "react-router-dom";

export class Header extends Component {
  render() {
    return (
        <nav className="navbar navbar-expand-sm navbar-dark bg-primary" style={{height: "4rem", width: "100%", position: "fixed", zIndex: "1"}}>
            <a className="navbar-brand" href="/">Elections Simulator</a>
            <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarColor01" aria-controls="navbarColor01" aria-expanded="false" aria-label="Toggle navigation">
                <span className="navbar-toggler-icon"></span>
            </button>

            <div className="collapse navbar-collapse" id="navbarColor01" style={{textAlign: "center"}}>
                <ul className="navbar-nav mr-auto">
                  <li className="nav-item active">
                    <a className="nav-link" href="#"> Home <span className="sr-only">(current)</span></a>
                  </li>
                  <li className="nav-item active">
                    <a className="nav-link" href="#/dists"> Distributions <span className="sr-only">(current)</span></a>
                  </li>
                </ul>
            </div>
        </nav>
    )
  }
}

export default Header
