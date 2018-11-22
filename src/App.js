import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import UploadForm from './Home';

// const {app} = window.require('electron').remote;

class App extends Component {
  render() {
    return (
      <div className="App">
        <div className="jumbotron">
          <h1>COMP1005 Marking</h1>
        </div>

        <UploadForm/>
      </div>
    );
  }
}

export default App;
