import React from 'react';
import './App.css';
import Header from './Page/Header';
import {BrowserRouter as Router, Route, Link} from 'react-router-dom';
import {About, MapInfo, Recommand} from './Page';

function ARoutePage() {


  return (
    <Router>
      <div className="App"> 
        <div className="App-Header"><Header /></div>
        <div className ="App-Body">
          <Route exact path ='/' component ={About}/>
          <Route exact path ='/about' component ={About}/>
          <Route path ='/map' component={MapInfo}/>
          <Route path ='/recommand' component={Recommand}/>
        </div>       
      </div>
    </Router>
  );
}

export default ARoutePage;
