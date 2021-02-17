import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import './App.css'
import Header from './Page/Header/Header'
import About from './Page/Body/About'
import MapInfo from './Page/Body/MapInfo' 

//import GraphArea from './GraphArea';

class App extends Component {
  render() {

    return (

      <Router>

        <div className="App">

          {/* Header */}
          <div className="App-Header">
            <Header />
          </div>

          {/* Body */}
          <div className="App-Body">
            <Route exact path='/' component={About} />
            <Route exact path='/about' component={About} />
            {/* <Route path='/map' component={MapInfo} /> */}
          </div>

          {/*<Footer/>*/}
          
        </div>

      </Router>

      //<GraphArea />
    )
  }
}

export default App;