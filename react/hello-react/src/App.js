import React from 'react';

import logo from './img/logo_hanbang.png';
import './App.css';

function App() {
  return (
    <div>
      <header>
        <div>
          <img src={logo} className="App-logo" alt="logo"/>
          <hr/>
        </div>
      </header>
    </div>



    /*
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
    */
  );
}

export default App;
