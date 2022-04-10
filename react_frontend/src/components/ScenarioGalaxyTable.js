import React from "react";

export function ScenarioGalaxyTable(props) {
    return (
        <div>
            <table>
                <tr>
                    <th>Planet</th>
                    <th>Neighbors</th>
                    <th>Days with bounty hunters</th>
                </tr>
                <tbody>
                {props.planets.map(planet => (
                    <tr>
                    <td>{planet}</td>
                    <td>
                        {Object.keys(props.neighbors[planet]).map(neighbor => (
                        <p>{neighbor} ({props.neighbors[planet][neighbor]} days)</p>
                        ))}
                    </td>
                    <td>{props.scenarioDays[planet]}</td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );
}