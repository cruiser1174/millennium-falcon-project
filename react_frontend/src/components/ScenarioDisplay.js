import React from "react";
import { ScenarioDetails } from "./ScenarioDetails";
import { ScenarioGalaxyTable } from "./ScenarioGalaxyTable";

export function ScenarioDisplay(props) {
    return (
        <div className="scenario-section">
            <h2 id="display-title" className='jedi-title'>Scenario details</h2>
            <div className="scenario-display">
                <ScenarioDetails 
                    startPlanet={props.startPlanet} 
                    destinationPlanet={props.destinationPlanet} 
                    fuelCapacity={props.fuelCapacity} 
                    timeLimit={props.timeLimit}/>
                <ScenarioGalaxyTable planets={props.planets} neighbors={props.neighbors} scenarioDays={props.scenarioDays} />
            </div>
        </div>
        
    );
}