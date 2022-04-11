import '../styles/App.css';
import { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import { CompareScenarioGalaxy } from '../components/CompareScenarioGalaxy';
import { Odds } from '../components/Odds';
import optimism from '../images/optimism.gif';
import yehaw from '../images/yehaw.gif';
import doomed from '../images/doomed.gif';
import { SelectionSection } from '../components/SelectionSection';
import { ScenarioDisplay } from '../components/ScenarioDisplay';
import { LoadingScreen } from '../components/LoadingScreen';


function App() {
  /*  state variables to hold data from server and elected scenarios/galaxies from user*/
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


  /*  on start-up get the availale galaxy and scenario data from the backend */
  useEffect(() => {
    fetch('/galaxy-api').then(result => result.json()).then(data => {
      setGalaxies(data.galaxies);
      setScenarios(data.scenarios);
    });
  }, []);

  /*  async function to calculate the odds for the selected galaxy/scenario - sends the 
      selected scenario to the server, and then waits for the optimal path to be returned, 
      setting the route and odds state variables */
  const getOdds = useCallback(async () => {
    const dataToPost = {
      galaxy: selectedGalaxy,
      scenario: selectedScenario
    };

    const response = await axios.post('/calculate-odds-api', dataToPost);
    setRoute(response.data.path_data);
    setOdds(response.data.odds);
  }, [selectedGalaxy, selectedScenario])

  /*  If a valid scenario-galaxy combination has been selected from the dropdowns, calculate the odds/path which will then be rendered */
  useEffect(() => {
    if (selectedGalaxy && selectedScenario && selectedScenarioPlanets.every(planet => selectedGalaxyPlanets.includes(planet))) {
      getOdds();
    } else {
      setOdds(null);
    }
  }, [selectedGalaxy, selectedScenario, selectedGalaxyPlanets, selectedScenarioPlanets, getOdds])

  /*  Sets the display image to go along with the rendering of the odds */
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

  /*  function to set state galaxy varables when user changes selection from dropdown */
  function updateSelectedGalaxy(newGalaxy) {
    setSelectedGalaxy(newGalaxy);
    setSelectedGalaxyPlanets(galaxies[newGalaxy].planets);
    setSelectedNeighborData(galaxies[newGalaxy].neighbors);
  };

  /*  function to set state scenario varables when user changes selection from dropdown */
  function updateSelectedScenario(newScenario) {
    setSelectedScenario(newScenario);
    setSelectedScenarioPlanets(Object.keys(scenarios[newScenario].planets));
    setSelectedScenarioDays(scenarios[newScenario].planets);
  };

  function handleFileUpload(newFile) {
    setFile(newFile);
  };

  /*  async function to upload a new scenario to the server - sends the 
      scenario to the server, and then waits it to be confirmed in the backend 
      and have the new list of scenarios returned, resetting the state variable 
      and alertig the user if the scenario name was changed */
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

  /*  If the galaxy/scenario data has not been retrieved from the server yet, display a loading screen */
  if (!galaxies || !scenarios) {
    return (
      <LoadingScreen/>
    );
  } else{
    return (
      <div className="App">
        <body className="App-body">
            {/* section for selecting scenario and uploading file */}
          <SelectionSection 
            galaxies={Object.keys(galaxies)} 
            scenarios={Object.keys(scenarios)}
            updateSelectedGalaxy={updateSelectedGalaxy}
            updateSelectedScenario={updateSelectedScenario}
            handleSubmit={handleFileSubmit}
            handleUpload={handleFileUpload}
            file={file}/> 
        
            {/* section for displaying the selected scenario */}
          {(selectedGalaxy && selectedScenario) && (
            selectedScenarioPlanets.every(planet => selectedGalaxyPlanets.includes(planet)) ? 
              <ScenarioDisplay 
                planets={selectedGalaxyPlanets} 
                neighbors={selectedNeighborData} 
                scenarioDays={selectedScenarioDays}
                startPlanet={galaxies[selectedGalaxy].departure}
                destinationPlanet={galaxies[selectedGalaxy].arrival}
                fuelCapacity={galaxies[selectedGalaxy].autonomy}
                timeLimit={scenarios[selectedScenario].countdown}/> :
              <CompareScenarioGalaxy galaxy={selectedGalaxy} galaxyPlanets={selectedGalaxyPlanets} scenario={selectedScenario} scenarioPlanets={selectedScenarioPlanets} />
          )}
            {/* section for displaying the odds of success */}
          {!isNaN(parseInt(odds)) && (
            <Odds odds={odds} route={route} image={displayImage}/>
          )}    
        </body>
      </div>
    );
  }
}

export default App;
