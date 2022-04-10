import '../App.css';
import { useEffect, useState } from 'react';
import axios from 'axios';
import { Dropdown } from '../components/Dropdown';
import { SubmitScenarioForm } from '../components/SubmitScenarioForm';
import { jsx } from '@emotion/react';
import { ScenarioGalaxyTable } from '../components/ScenarioGalaxyTable';
import { CompareScenarioGalaxy } from '../components/CompareScenarioGalaxy';
import { Odds } from '../components/Odds';
import { Route } from '../components/Route';
import logo from '../logo.svg';
import certainty from '../certainty.gif';
import { SelectionSection } from '../components/SelectionSection';
import { ScenarioDisplay } from '../components/ScenarioDisplay';


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
  const [file, setFile] = useState()

  useEffect(() => {
    fetch('/galaxy-api').then(result => result.json()).then(data => {
      setGalaxies(data.galaxies);
      setScenarios(data.scenarios);
    });
  }, []);

  function updateSelectedGalaxy(newGalaxy) {
    setSelectedGalaxy(newGalaxy);
    setSelectedGalaxyPlanets(galaxies[newGalaxy].planets);
    setSelectedNeighborData(galaxies[newGalaxy].neighbors);
  };

  function updateSelectedGalaxyPlanets(newPlanets) {
    setSelectedGalaxyPlanets(newPlanets);
  };

  function updateSelectedScenario(newScenario) {
    setSelectedScenario(newScenario);
    setSelectedScenarioPlanets(Object.keys(scenarios[newScenario].planets));
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
    setRoute(response.data.path_data);
  };

  function handleFileUpload(event) {
    setFile(event.target.files[0])
  };

  function handleFileSubmit(event) {
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
  } else{
    return (
      <div className="App">
        <header className="App-header">
          <h1 id="title">Kessel Run odds calculator</h1>
          {<SelectionSection 
            galaxies={Object.keys(galaxies)} 
            scenarios={Object.keys(scenarios)}
            updateSelectedGalaxy={updateSelectedGalaxy}
            updateSelectedScenario={updateSelectedScenario}
            onSubmit={handleFileSubmit}
            handleUpload={handleFileUpload}/> }

          {(selectedGalaxy && selectedScenario) && (
            selectedScenarioPlanets.every(planet => selectedGalaxyPlanets.includes(planet)) ? 
              <div>
                <ScenarioDisplay 
                  planets={selectedGalaxyPlanets} 
                  neighbors={selectedNeighborData} 
                  scenarioDays={selectedScenarioDays}
                  startPlanet={galaxies[selectedGalaxy].departure}
                  destinationPlanet={galaxies[selectedGalaxy].arrival}
                  fuelCapacity={galaxies[selectedGalaxy].autonomy}
                  timeLimit={scenarios[selectedScenario].countdown}/>

                <button onClick={getOdds}>Calculate Odds</button>
              </div> :
              <CompareScenarioGalaxy galaxy={selectedGalaxy} galaxyPlanets={selectedGalaxyPlanets} scenario={selectedScenario} scenarioPlanets={selectedScenarioPlanets} />
          )}

          {!isNaN(parseInt(odds)) && (
            <div>
              <Odds odds={odds}/>
              <p>{typeof odds == 'number'}</p>
              {odds > 0 ? <Route route={route} /> : <img src={certainty}/>}
            </div>
            )}    
        </header>
      </div>
    );
  }
}

export default App;
