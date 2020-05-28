import React,{Component} from 'react';
import './App.css';
import Header from './Page/Header';
import Footer from './Page/Footer';
import {BrowserRouter as Router, Route, Link} from 'react-router-dom';
import {About, MapInfo} from './Page';

function App() {


  return (
    <Router>
      <div className="App"> 
        <div className="App-Header"><Header /></div>
        <div className ="App-Body">
          <Route exact path ='/' component ={About}/>
          <Route exact path ='/about' component ={About}/>
          <Route path ='/map' component={MapInfo}/>
        </div>
        {/*<Footer/>*/}
      </div>
    </Router>
  );
}

export default App;
