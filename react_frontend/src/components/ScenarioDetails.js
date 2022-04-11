import React from "react";

export function ScenarioDetails(props) {
    return (
        <div className="scenario-details">
            <text className="scenario-detail" id="start-planet">Start planet: {props.startPlanet}</text>
            <text className="scenario-detail" id="destination-planet">Destination planet: {props.destinationPlanet}</text>
            <text className="scenario-detail" id="time-limit">Time limit: {props.timeLimit} days</text>
            <text className="scenario-detail" id="fuel-capacity">Fuel capacity: {props.fuelCapacity} days</text>
        </div>
    );
}