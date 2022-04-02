import './App.css';
import { useEffect, useState } from 'react';
import axios from 'axios';
import { Dropdown } from './Dropdown';

function App() {
  const [galaxies, setGalaxies] = useState(null);
  const [scenarios, setScenarios] = useState(null);
  const [selectedGalaxy, setSelectedGalaxy] = useState(null);
  const [selectedScenario, setSelectedScenario] = useState(null);
  const [odds, setOdds] = useState(null);

  useEffect(() => {
    fetch('/galaxy-api').then(result => result.json()).then(data => {
      setGalaxies(data.galaxies);
    });
  }, []);

  useEffect(() => {
    fetch('/galaxy-api').then(result => result.json()).then(data => {
      setScenarios(data.scenarios);
    });
  }, []);

  useEffect(() => {
    if (galaxies) {
      updateSelectedGalaxy(Object.keys(galaxies)[0]);
    };
  }, [galaxies]);

  useEffect(() => {
    if (scenarios) {
      updateSelectedScenario(Object.keys(scenarios)[0]);
    };
  }, [scenarios]);

  function updateSelectedGalaxy(newGalaxy) {
    setSelectedGalaxy(newGalaxy);
  };

  function updateSelectedScenario(newScenario) {
    setSelectedScenario(newScenario);
  };

  //if (galaxies) {
  //  updateSelectedGalaxy(Object.keys(galaxies)[0])
  //};

  function calculateOdds() {
    const dataToPost = {
      galaxy: selectedGalaxy,
      scenario: scenarios[selectedScenario]
    };

    axios.post('/calculate-odds-api', dataToPost).then( function (response) {
      console.log(response);
    }).catch(function (error) {
      console.log(error)
    });

  }

  if (!galaxies && !scenarios) {
    return (
      <div className="App">
        <header className="App-header">
          <p>Loading...</p>
        </header>
      </div>
    );
  } else{
    return (
      <div className="App">
        <header className="App-header">
          <p>Choose a galaxy:</p>
          {galaxies && <Dropdown items={Object.keys(galaxies)} onChange={updateSelectedGalaxy} />}
  
          <p>Choose a scenario:</p>
          {scenarios && <Dropdown items={Object.keys(scenarios)} onChange={updateSelectedScenario} />}
  
          {selectedGalaxy && 
          <div>
            <p> Selected Galaxy: {selectedGalaxy} </p>
            <p> Planets in Galaxy: 
              <ul>
              {galaxies[selectedGalaxy].planets.map(planet => (
                <li>{planet}</li>
              ))}
              </ul>
            </p>
            <p> Departure Planet: {galaxies[selectedGalaxy].departure} </p>
            <p> Destination Planet: {galaxies[selectedGalaxy].arrival} </p>
            <p> Autonomy (days): {galaxies[selectedGalaxy].autonomy} </p>
          </div>}
  
          {selectedScenario && 
          <div>
            <p> Selected Scenario: {selectedScenario} </p>
            <p> Time Limit: {scenarios[selectedScenario].countdown} </p>
          </div>}
  
          <button onClick={calculateOdds}>Calculate Odds</button>
          {odds && <p>Odds of success: {odds}</p>}
  
          
        </header>
      </div>
    );
  }
}

export default App;
