/** @jsxImportSource @emotion/react */
import React from "react";

export function ScenarioDetails(props) {
    const detailsStyle = {
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-around',
        alignItems: 'flex-start',
        margin: '0rem 1.5rem',
        width: '30%'
    }
    return (
        <div className="scenarioDetails" css={detailsStyle}>
            <h4>Start planet: {props.startPlanet}</h4>
            <h4>Destination planet: {props.destinationPlanet}</h4>
            <h4>Time limit: {props.timeLimit} days</h4>
            <h4>Fuel capacity: {props.fuelCapacity} days</h4>
        </div>
    );
}