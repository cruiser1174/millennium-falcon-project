/** @jsxImportSource @emotion/react */
import React from "react";

export function ScenarioGalaxyTable(props) {
    return (
        <table className="scenarioGalaxyTable" css={{width: '60%', margin: '0 1.5rem'}}>
            <colgroup>
                <col className="planets" css={{width: '20%'}} />
                <col className="neighbors" css={{width: '40%'}} />
                <col className="hunters" css={{width: '40%'}} />
            </colgroup>

            <thead>
                <tr>
                    <th col="planets" className="planets">Planets</th>
                    <th className="neighbors">Neighbors</th>
                    <th className="hunters">Days with bounty hunters</th>
                </tr>
            </thead>

            <tbody>
            {props.planets.map(planet => (
                <tr>
                <td className="planet">{planet}</td>
                <td className="neighbors">
                    {Object.keys(props.neighbors[planet]).map(neighbor => (
                    <p className="neighbor">{neighbor} ({props.neighbors[planet][neighbor]} days)</p>
                    ))}
                </td>
                <td className="hunterDays">{props.scenarioDays[planet]}</td>
                </tr>
            ))}
            </tbody>
        </table>
    );
}