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
  const [route, setRoute] = useState(null);
  const [days, setDays] = useState(null);
  const getOddsEffect = 0;

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

  async function calculateOdds() {
    const dataToPost = {
      galaxy: selectedGalaxy,
      scenario: scenarios[selectedScenario]
    };

    await axios.post('/calculate-odds-api', dataToPost).then(result => result.json()).then(data => {
      setOdds(data);
    });
  };

  async function getOdds() {
    await fetch(
      '/calculate-odds-api').then(
        result => result.json()).then(
          data => {setOdds(data);
    });
  };

  function makeOdds() {
    const dataToPost = {
      galaxy: selectedGalaxy,
      scenario: scenarios[selectedScenario]
    };

    axios.post('/calculate-odds-api', dataToPost).then(
      response => {
        setOdds(response.data.odds);
        setRoute(response.data.path);
        setDays(response.data.days)
      });
  };

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
  
          <button onClick={makeOdds}>Calculate Odds</button>
          {odds && <p>Odds of success: {odds}</p>}
          {route && <p>Route: {route}</p>}
          {days && <p>Days: {days}</p>}
  
          
        </header>
      </div>
    );
  }
}

export default App;
