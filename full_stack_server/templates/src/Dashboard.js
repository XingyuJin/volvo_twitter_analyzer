import React, { Component } from 'react';

import logo from './logo.svg';
import './assets/css/Dashboard.css';
import AccountAnalytics from './views/AccountAnalytics';
import MentionStatistics from './views/MentionStatistics';
import { Navbar, Nav }  from 'react-bootstrap';
import { Route, Switch, Redirect } from 'react-router-dom';
import { Link } from 'react-router-dom';



class Dashboard extends Component {


  constructor(props) {
    super(props);
    this.state = {
      isAA: true,
    }

  }

  toggle = () =>{
    const { isAA } = this.state;
    this.setState({
      isAA: !isAA,
    })
  }

  render() {

    const { isAA } = this.state;
    return (
      <div className="dashboard-container">
        <h2 className="dashboard-title"> Volvo Social Media (Twitter) Dashboard </h2>
        <Navbar bg="light" variant="light">
          <Nav className="mr-auto">
            <Nav.Link as={Link} to="/AccountAnalytics" key="AccountAnalytics" onClick={this.toggle} className={isAA ? "dashboard-nav-hover" : "dashboard-nav"}>Account Analytics</Nav.Link>
            <Nav.Link as={Link} to="/MentionStatistics" key="MentionStatistics" onClick={this.toggle} className={!isAA ? "dashboard-nav-hover" : "dashboard-nav"} >Mention Statistics</Nav.Link>
          </Nav>
        </Navbar>
        <Switch>
          <Route from="/AccountAnalytics" component={AccountAnalytics} key="AccountAnalytics" />
          <Route from="/MentionStatistics" component={MentionStatistics} key="MentionStatistics" />
        </Switch>
      </div>
    );
  }

}

export default Dashboard;


//
// <AccountAnalytics />
// <MentionStatistics />
