import React from "react";

export function ScenarioDetails(props) {
    return (
        <div className="scenario-details">
            <h4 className="scenario-detail" id="start-planet">Start planet: {props.startPlanet}</h4>
            <h4 className="scenario-detail" id="destination-planet">Destination planet: {props.destinationPlanet}</h4>
            <h4 className="scenario-detail" id="time-limit">Time limit: {props.timeLimit} days</h4>
            <h4 className="scenario-detail" id="fuel-capacity">Fuel capacity: {props.fuelCapacity} days</h4>
        </div>
    );
}