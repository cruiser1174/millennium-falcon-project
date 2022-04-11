import React from "react";

export function CompareScenarioGalaxy(props) {
    return (
        <div className="scenario-comparison">
            <h4 id="comparison-overview">
                A planet in the scenario is not in the selected galaxy (see planets highlighted in red). 
                Choose a scenario where all planets are in the selected galaxy. </h4>
            <div className="comparison-container">
                <div id="galaxy-planets-list" className="planet-list">
                    <h4 id="galaxy-list-header" className="planet-list-header"> Planets in Galaxy </h4>
                    {props.galaxyPlanets.map(planet => (
                        <p id={planet} className="planet">{planet}</p>
                    ))}
                </div>
                <div id="scenario-planets-list" className="planet-list">
                    <h4 id="scenario-list-header" className="planet-list-header"> Planets in Scenario </h4>
                    {props.scenarioPlanets.map(planet => (
                        props.galaxyPlanets.includes(planet) ? 
                        <p id={planet} className="planet">{planet}</p> :
                        <p id={planet} className="red-planet">{planet}</p>
                    ))}
                </div>
            </div>
        </div>
    )
}