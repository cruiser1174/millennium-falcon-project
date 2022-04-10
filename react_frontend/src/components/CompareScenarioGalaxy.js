/** @jsxImportSource @emotion/react */
import React from "react";

export function CompareScenarioGalaxy(props) {
    const comparisonStyle = {
        width: '55%',
        margin: '50px'}
    
    const comparisonListContainterStyle = {
        display: 'flex',
        justifyContent: 'center',
        margin: '20px 20px'
    }

    const containerListStyle = {
        margin: '10px 50px'
    }

    return (
        <div css = {comparisonStyle}>
            <h4> A planet in the scenario is not in the selected galaxy (see planets highlighted in red). Choose a scenario where all planets are in the selected galaxy. </h4>
            <div css = {comparisonListContainterStyle}>
                <div css = {containerListStyle}>
                    <h4> Planets in Galaxy </h4>
                    {props.galaxyPlanets.map(planet => (
                        <p>{planet}</p>
                    ))}
                </div>
                <div css = {containerListStyle}>
                    <h4> Planets in Scenario </h4>
                    {props.scenarioPlanets.map(planet => (
                        props.galaxyPlanets.includes(planet) ? 
                        <p>{planet}</p> :
                        <p css={{color: 'red'}}>{planet}</p>
                    ))}
                </div>
            </div>
        </div>
    )
}