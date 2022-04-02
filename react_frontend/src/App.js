import logo from './logo.svg';
import './App.css';
import { useState } from 'react';
import axios from 'axios';

function App() {
  const [galaxyData, setGalaxyData] = useState(null);


  function getGalaxyData() {
    fetch('/galaxy-api').then(result => result.json()).then(data => {
      setGalaxyData(data);
    });
  }

  function postEmpireData() {
    
    const dataToPost = {
      name: 'Empire Data',
      locations: {
        'planet': 1,
        'planet 2': 2
      }
    };

    axios.post('/send-bounty-hunters-api', dataToPost).then( function (response) {
      console.log(response);
    }).catch(function (error) {
      console.log(error)
    });
  }

  return (
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
        <p>Get data from server:</p>
        <button onClick={getGalaxyData}>Click to get galaxy data</button>
        {galaxyData && <div>
            <p>Galaxy data {JSON.stringify(galaxyData)}</p>
          </div>}
        
        <p>Post data to server:</p>
        <button onClick={postEmpireData}>Click to post empire data</button>
      </header>
    </div>
  );
}

export default App;
