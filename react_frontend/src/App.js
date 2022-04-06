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
  const [file, setFile] = useState()

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

  async function getExistingData() {
    const response = await axios.get('/galaxy-api');
    return response.data
  };

  async function createOdds() {

    const dataToPost = {
      galaxy: selectedGalaxy,
      scenario: scenarios[selectedScenario]
    };

    const response = await axios.post('/calculate-odds-api', dataToPost);
    setOdds(response.data.odds);
    setRoute(response.data.path);
    setDays(response.data.days)
  };

  function handleUpload(event) {
    setFile(event.target.files[0])
  };

  function handleSubmit(event) {
    event.preventDefault()
    const formData = new FormData();
    formData.append('file', file);
    formData.append('fileName', file.name);
    const config = {
      headers: {
        'content-type': 'multipart/form-data',
      },
    };
    axios.post('/upload-scenario-api', formData, config).then((response) => {
      console.log(response.data);
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

          <form onSubmit={handleSubmit}>
            <p>Or upload a new scenario:</p>
            <input type="file" onChange={handleUpload}/>
            <button type="submit">Upload</button>
        </form>
  
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
  
          <button onClick={createOdds}>Calculate Odds</button>
          {odds && <p>Odds of success: {odds}</p>}
          {route && <p>Route: {route}</p>}
          {days && <p>Days: {days}</p>}
  
          
        </header>
      </div>
    );
  }
}

export default App;
