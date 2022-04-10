/** @jsxImportSource @emotion/react */
import React from "react";

export function ScenarioDetails(props) {
    const detailsStyle = {
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-around',
        alignItems: 'flex-start',
        marginRight: '5rem'
    }
    return (
        <div className="scenarioDetails" css={detailsStyle}>
            <h3>Start planet: {props.startPlanet}</h3>
            <h3>Destination planet: {props.destinationPlanet}</h3>
            <h3>Time limit: {props.timeLimit} days</h3>
            <h3>Fuel capacity: {props.fuelCapacity} days</h3>
        </div>
    );
}