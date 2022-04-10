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
import optimism from '../optimism.gif';
import yehaw from '../yehaw.gif';
import doomed from '../doomed.gif';
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
  const [file, setFile] = useState();
  const [displayImage, setDisplayImage] = useState();

  useEffect(() => {
    fetch('/galaxy-api').then(result => result.json()).then(data => {
      setGalaxies(data.galaxies);
      setScenarios(data.scenarios);
    });
  }, []);

  useEffect(() => {
    if (selectedGalaxy && selectedScenario && selectedScenarioPlanets.every(planet => selectedGalaxyPlanets.includes(planet))) {
      getOdds();
    } else {
      setOdds(null);
    }
  }, [selectedGalaxy, selectedScenario])

  useEffect(() => {
    if (isNaN(parseInt(odds))) {
      setDisplayImage(null);
    } else if (odds === 100) {
      setDisplayImage(yehaw);
    } else if (odds === 0) {
      setDisplayImage(doomed);
    } else {
      setDisplayImage(optimism);
    }
  }, [odds])

  function updateSelectedGalaxy(newGalaxy) {
    setSelectedGalaxy(newGalaxy);
    setSelectedGalaxyPlanets(galaxies[newGalaxy].planets);
    setSelectedNeighborData(galaxies[newGalaxy].neighbors);
  };

  function updateSelectedScenario(newScenario) {
    setSelectedScenario(newScenario);
    setSelectedScenarioPlanets(Object.keys(scenarios[newScenario].planets));
    setSelectedScenarioDays(scenarios[newScenario].planets);
  };

  async function getOdds() {

    const dataToPost = {
      galaxy: selectedGalaxy,
      scenario: selectedScenario
    };

    const response = await axios.post('/calculate-odds-api', dataToPost);
    setRoute(response.data.path_data);
    setOdds(response.data.odds);
  };

  function handleFileUpload(newFile) {
    setFile(newFile);
  };

  async function handleFileSubmit(newFile) {
    const formData = new FormData();
    formData.append('file', newFile);
    formData.append('fileName', newFile.name);
    const config = {
      headers: {
        'content-type': 'multipart/form-data',
      },
    };

    const response = await axios.post('/upload-scenario-api', formData, config);
    setScenarios(response.data.scenarios);
    alert(response.data.alert);

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
          <div>
          <SelectionSection 
            galaxies={Object.keys(galaxies)} 
            scenarios={Object.keys(scenarios)}
            updateSelectedGalaxy={updateSelectedGalaxy}
            updateSelectedScenario={updateSelectedScenario}
            handleSubmit={handleFileSubmit}
            handleUpload={handleFileUpload}
            file={file}/> 
          </div>
          

          {(selectedGalaxy && selectedScenario) && (
            selectedScenarioPlanets.every(planet => selectedGalaxyPlanets.includes(planet)) ? 
              <div>
                <h2 id="title">Scenario details</h2>
                <ScenarioDisplay 
                  planets={selectedGalaxyPlanets} 
                  neighbors={selectedNeighborData} 
                  scenarioDays={selectedScenarioDays}
                  startPlanet={galaxies[selectedGalaxy].departure}
                  destinationPlanet={galaxies[selectedGalaxy].arrival}
                  fuelCapacity={galaxies[selectedGalaxy].autonomy}
                  timeLimit={scenarios[selectedScenario].countdown}/>

                {/*<button onClick={getOdds}>Calculate Odds</button>*/}
              </div> :
              <CompareScenarioGalaxy galaxy={selectedGalaxy} galaxyPlanets={selectedGalaxyPlanets} scenario={selectedScenario} scenarioPlanets={selectedScenarioPlanets} />
          )}

          {!isNaN(parseInt(odds)) && (
            <div>
              <h2 id="title">odds of success</h2>
              <Odds odds={odds} route={route} image={displayImage}/>
            </div>
            )}    
        </header>
      </div>
    );
  }
}

export default App;
