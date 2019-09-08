import React, { Component, Fragment } from 'react';
import ReactDOM from 'react-dom';
import { HashRouter as Router, Route, Switch, Redirect } from "react-router-dom";

import { Provider } from 'react-redux';
import store from '../store';

import Header from './layout/Header';
import Dashboard from './Dashboard';
import Results from './Results/Results';
import DirectRes from './Results/DirectRes';
import Distributions from './Distributions';

class App extends React.Component {
	render(){
		return(
			<Provider store={store}>
				<Router>
					<Fragment>
						<Header />
						<Switch>
							<Route exact path="/" component={Dashboard} />
							<Route exact path="/results" component={Results} />
							<Route exact path="/direct_res" component={DirectRes} />
							<Route exact path="/direct_res/:systems/:n_voters/:n_vacancies/:candidates/:names/:tc/:mc/:tv/:mv/:coal/:voters/:seed" component={DirectRes} />
							<Route exact path="/dists" component={Distributions} />
						</Switch>
					</Fragment>
				</Router>
			</Provider>
		)
	}
}

ReactDOM.render(<App />, document.getElementById('app'));