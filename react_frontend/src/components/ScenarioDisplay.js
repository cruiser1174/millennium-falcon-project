/** @jsxImportSource @emotion/react */
import React from "react";
import { ScenarioDetails } from "./ScenarioDetails";
import { ScenarioGalaxyTable } from "./ScenarioGalaxyTable";

export function ScenarioDisplay(props) {
    const scenarioDisplayStyle = {
        display: 'flex',
        width: '100%',
        justifyContent: 'space-around',
        flexFlow: 'row wrap'
    }

    return (
        <div className="scenarioDisplay" css={scenarioDisplayStyle}>
            <ScenarioDetails 
                startPlanet={props.startPlanet} 
                destinationPlanet={props.destinationPlanet} 
                fuelCapacity={props.fuelCapacity} 
                timeLimit={props.timeLimit}/>
            <ScenarioGalaxyTable planets={props.planets} neighbors={props.neighbors} scenarioDays={props.scenarioDays} />
        </div>
    );
}