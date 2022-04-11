import React from "react";

export function ScenarioGalaxyTable(props) {
    return (
        <table id="scenario-comparison-table" className="scenario-galaxy-table">
            <colgroup>
                <col id="planets-col" className="planets"/>
                <col id="neighbors-col" className="neighbors"/>
                <col id="hunters-col" className="hunters"/>
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
                        props.neighbors[planet][neighbor] > 1 ? 
                            <p className="neighbor">{neighbor} ({props.neighbors[planet][neighbor]} days)</p> :
                            <p className="neighbor">{neighbor} ({props.neighbors[planet][neighbor]} day)</p>
                    ))}
                </td>
                <td className="hunterDays">{props.scenarioDays[planet]}</td>
                </tr>
            ))}
            </tbody>
        </table>
    );
}