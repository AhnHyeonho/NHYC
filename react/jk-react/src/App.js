import React, { Component } from 'react';
import './App.css';
import Header from './Page/Header';
import Footer from './Page/Footer';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import { About, MapInfo, Recommand } from './Page';

function App() {


  return (
    <Router>

      {/* header */}
      <div className="App-Header">
        <Header />
      </div>

      {/* body */}
      <div className="App-Body">
        <Route exact path='/' component={About} />
        <Route exact path='/about' component={About} />
        <Route path='/map' component={MapInfo} />
        <Route path='/recommand' component={Recommand} />
      </div>

      {/* footer */}
    </Router>
  );
}

export default App;
