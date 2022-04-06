import './App.css';
import { useEffect, useState } from 'react';
import axios from 'axios';
import { Dropdown } from './Dropdown';
import { useAlert } from 'react-alert';

function App() {
  const [galaxies, setGalaxies] = useState(null);
  const [scenarios, setScenarios] = useState(null);
  const [selectedNeighborData, setSelectedNeighborData] = useState(null);
  const [selectedGalaxy, setSelectedGalaxy] = useState(null);
  const [selectedGalaxyPlanets, setSelectedGalaxyPlanets] = useState(null);
  const [selectedScenario, setSelectedScenario] = useState(null);
  const [selectedScenarioPlanets, setSelectedScenarioPlanets] = useState(null);
  const [selectedScenarioDays, setSelectedScenarioDays] = useState(null);
  const [odds, setOdds] = useState(null);
  const [route, setRoute] = useState(null);
  const [days, setDays] = useState(null);
  const [file, setFile] = useState()

  useEffect(() => {
    fetch('/galaxy-api').then(result => result.json()).then(data => {
      setGalaxies(data.galaxies);
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
    updateSelectedGalaxyPlanets(galaxies[newGalaxy].planets);
    setSelectedNeighborData(galaxies[newGalaxy].neighbors);
  };

  function updateSelectedGalaxyPlanets(newPlanets) {
    setSelectedGalaxyPlanets(newPlanets);
  };

  function updateSelectedScenario(newScenario) {
    setSelectedScenario(newScenario);
    updateSelectedScenarioPlanets(Object.keys(scenarios[newScenario].planets));
    setSelectedScenarioDays(scenarios[newScenario].planets);
  };

  function updateSelectedScenarioPlanets(newPlanets) {
    setSelectedScenarioPlanets(newPlanets);
  };

  async function getOdds() {

    const dataToPost = {
      galaxy: selectedGalaxy,
      scenario: selectedScenario
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
      setScenarios(response.data.scenarios);
      alert(response.data.alert);
    });

  };

  if (!galaxies || !scenarios) {
    return (
      <div className="App">
        <header className="App-header">
          <p>Loading Galaxies and Scenarios...</p>
        </header>
      </div>
    );
  } else if (!galaxies) {
    return (
      <div className="App">
        <header className="App-header">
          <p>Loading Galaxies...</p>
        </header>
      </div>
    );
  } else if (!scenarios) {
    return (
      <div className="App">
        <header className="App-header">
          <p>Loading Scenarios...</p>
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
            <p> Planets in Scenario: 
              <ul>
                {Object.keys(scenarios[selectedScenario].planets).map(planet => (
                  <li>{planet}</li>
                ))}
              </ul>
            </p>
            <p>planets in scenario: {selectedScenarioPlanets}</p>
            <p>type: {typeof(selectedScenarioPlanets)}</p>
            <p>planets in galaxy: {selectedGalaxyPlanets}</p>
            <p>type: {typeof(selectedGalaxyPlanets)}</p>
            <p>neighbors: {JSON.stringify(selectedNeighborData)}</p>
          </div>}

          {(selectedGalaxy && selectedScenario && selectedScenarioPlanets.every(planet => selectedGalaxyPlanets.includes(planet))) ?
            (<table>
              <tr>
                <th>Planet</th>
                <th>Neighbors</th>
                <th>Days with bounty hunters</th>
              </tr>
              <tbody>
                {galaxies[selectedGalaxy].planets.map(planet => (
                  <tr>
                    <td>{planet}</td>
                    <td>
                      {Object.keys(galaxies[selectedGalaxy].neighbors[planet]).map(neighbor => (
                        <p>{neighbor} ({galaxies[selectedGalaxy].neighbors[planet][neighbor]} days)</p>
                      ))}
                    </td>
                    <td>{selectedScenarioDays[planet]}</td>
                  </tr>
                ))}
              </tbody>
            </table>) : <p>no</p>
          }
  
          <button onClick={getOdds}>Calculate Odds</button>
          {odds && <p>Odds of success: {odds}</p>}
          {route && <p>Route: {route}</p>}
          {days && <p>Days: {days}</p>}
  
          
        </header>
      </div>
    );
  }
}

export default App;
