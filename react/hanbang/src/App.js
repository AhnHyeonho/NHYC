import React, { Component } from 'react';
import DefaultMap from './Components/DefaultMap';
import SearchBar from './Components/SearchBar';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/css/bootstrap-theme.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <SearchBar/>
        <DefaultMap/>
      </div>
    );
  } 
}

export default App;
