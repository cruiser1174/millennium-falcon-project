/** @jsxImportSource @emotion/react */
import React from "react";

export function CompareScenarioGalaxy(props) {
    return (
        <div css = {{
            width: '55%',
            margin: '50px'}}>
            <p> A planet in the scenario is not in the selected galaxy (see planets highlighted in red). Choose a scenario where all planets are in the selected galaxy. </p>
            <div css = {{
                display: 'flex',
                justifyContent: 'space-around',
                margin: '20px 20px'
            }}>
                <div css = {{
                    margin: '20px 20px'
                }}>
                    <h4> Planets in Galaxy </h4>
                    {props.galaxyPlanets.map(planet => (
                        <p>{planet}</p>
                    ))}
                </div>
                <div css = {{
                    margin: '20px 20px'
                }}>
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